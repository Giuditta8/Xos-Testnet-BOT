# -*- coding: utf-8 -*-
"""
JSON-RPC client for the XOS blockchain testnet.

Handles connection management, request serialization, retry logic,
and provides typed helpers for common on-chain operations.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Union


DEFAULT_RPC_URL = "https://xos-testnet.rpc.caldera.xyz/http"
DEFAULT_CHAIN_ID = 37714555429
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1.5


class RPCError(Exception):
    """Raised when the JSON-RPC endpoint returns an error object."""
    def __init__(self, code: int, message: str, data: Any = None) -> None:
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"RPC error {code}: {message}")


class XosRPCClient:
    """Minimal JSON-RPC 2.0 client for the XOS testnet."""

    def __init__(
        self,
        rpc_url: str = DEFAULT_RPC_URL,
        chain_id: int = DEFAULT_CHAIN_ID,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self.rpc_url = rpc_url
        self.chain_id = chain_id
        self.timeout = timeout
        self.max_retries = max_retries
        self._req_id = 0

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    def _raw_request(self, method: str, params: Union[list, dict, None] = None) -> Any:
        """Send a single JSON-RPC request with retry and backoff."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": self._next_id(),
        }
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(self.rpc_url, data=body, headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if "error" in data and data["error"]:
                    err = data["error"]
                    raise RPCError(err.get("code", -1), err.get("message", "unknown"), err.get("data"))
                return data.get("result")
            except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(RETRY_BACKOFF_BASE ** attempt)

        raise ConnectionError(f"RPC request failed after {self.max_retries + 1} attempts: {last_error}")

    # --- high-level helpers ---------------------------------------------------

    def get_chain_id(self) -> int:
        """Return the chain ID reported by the node."""
        raw = self._raw_request("eth_chainId")
        return int(raw, 16)

    def get_block_number(self) -> int:
        """Return the latest block number."""
        raw = self._raw_request("eth_blockNumber")
        return int(raw, 16)

    def get_balance(self, address: str, block: str = "latest") -> int:
        """Return the balance of *address* in wei."""
        raw = self._raw_request("eth_getBalance", [address, block])
        return int(raw, 16)

    def get_transaction_count(self, address: str, block: str = "latest") -> int:
        """Return the nonce (transaction count) for *address*."""
        raw = self._raw_request("eth_getTransactionCount", [address, block])
        return int(raw, 16)

    def get_gas_price(self) -> int:
        """Return the current gas price in wei."""
        raw = self._raw_request("eth_gasPrice")
        return int(raw, 16)

    def send_raw_transaction(self, signed_tx_hex: str) -> str:
        """Broadcast a signed transaction and return the tx hash."""
        return self._raw_request("eth_sendRawTransaction", [signed_tx_hex])

    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Return the receipt for *tx_hash*, or None if not yet mined."""
        return self._raw_request("eth_getTransactionReceipt", [tx_hash])

    def get_block_by_number(self, number: int, full_txs: bool = False) -> Dict[str, Any]:
        """Return block data by number."""
        hex_num = hex(number)
        return self._raw_request("eth_getBlockByNumber", [hex_num, full_txs])

    def call(self, tx_object: Dict[str, str], block: str = "latest") -> str:
        """Execute an eth_call (read-only contract call)."""
        return self._raw_request("eth_call", [tx_object, block])

    def estimate_gas(self, tx_object: Dict[str, str]) -> int:
        """Estimate gas for a transaction."""
        raw = self._raw_request("eth_estimateGas", [tx_object])
        return int(raw, 16)

    def wait_for_receipt(self, tx_hash: str, poll_interval: float = 2.0,
                         max_wait: float = 120.0) -> Dict[str, Any]:
        """Poll until the transaction receipt is available or *max_wait* expires."""
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            receipt = self.get_transaction_receipt(tx_hash)
            if receipt is not None:
                return receipt
            time.sleep(poll_interval)
        raise TimeoutError(f"Transaction {tx_hash} not mined within {max_wait}s")
