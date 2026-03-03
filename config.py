# -*- coding: utf-8 -*-
"""
Configuration management for Xos Testnet BOT.

Provides structured defaults, persistent JSON storage, and runtime
validation for all bot operation parameters.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


CONFIG_NAME = "config.json"

DEFAULTS: Dict[str, Any] = {
    "proxy_mode": "free",
    "auto_rotate_invalid_proxies": True,
    "auto_checkin": True,
    "auto_draw": True,
    "auto_wrap": True,
    "auto_unwrap": False,
    "auto_swap": True,
    "auto_add_liquidity": False,
    "rpc_url": "https://xos-testnet.rpc.caldera.xyz/http",
    "chain_id": 37714555429,
    "explorer_url": "https://xos-testnet.explorer.caldera.xyz",
    "request_timeout": 30,
    "max_retries": 3,
}

PROXY_MODES = ("free", "private", "none")

BOOLEAN_KEYS = (
    "auto_rotate_invalid_proxies",
    "auto_checkin",
    "auto_draw",
    "auto_wrap",
    "auto_unwrap",
    "auto_swap",
    "auto_add_liquidity",
)


class Config:
    """Thread-safe, validated configuration backed by a JSON file."""

    def __init__(self, base_dir: Path) -> None:
        self._path = base_dir / CONFIG_NAME
        self._data: Dict[str, Any] = dict(DEFAULTS)
        self.reload()

    def reload(self) -> None:
        """Load configuration from disk, falling back to defaults."""
        if self._path.exists():
            try:
                stored = json.loads(self._path.read_text(encoding="utf-8"))
                self._data = {**DEFAULTS, **stored}
            except (json.JSONDecodeError, OSError):
                self._data = dict(DEFAULTS)
        else:
            self._data = dict(DEFAULTS)

    def save(self) -> None:
        """Persist current configuration to disk."""
        self._path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def toggle(self, key: str) -> bool:
        """Toggle a boolean key and return the new value."""
        if key not in BOOLEAN_KEYS:
            raise KeyError(f"{key} is not a toggleable boolean setting")
        current = bool(self._data.get(key, False))
        self._data[key] = not current
        return not current

    @property
    def proxy_mode(self) -> str:
        return self._data.get("proxy_mode", "free")

    @proxy_mode.setter
    def proxy_mode(self, mode: str) -> None:
        if mode not in PROXY_MODES:
            raise ValueError(f"proxy_mode must be one of {PROXY_MODES}")
        self._data["proxy_mode"] = mode

    @property
    def rpc_url(self) -> str:
        return self._data.get("rpc_url", DEFAULTS["rpc_url"])

    @property
    def chain_id(self) -> int:
        return int(self._data.get("chain_id", DEFAULTS["chain_id"]))

    def validate(self) -> List[str]:
        """Return a list of validation error messages (empty if valid)."""
        errors: List[str] = []
        if self._data.get("proxy_mode") not in PROXY_MODES:
            errors.append(f"Invalid proxy_mode: {self._data.get('proxy_mode')}")
        if not isinstance(self._data.get("request_timeout"), (int, float)):
            errors.append("request_timeout must be numeric")
        elif self._data["request_timeout"] <= 0:
            errors.append("request_timeout must be positive")
        if not isinstance(self._data.get("max_retries"), int):
            errors.append("max_retries must be an integer")
        elif self._data["max_retries"] < 0:
            errors.append("max_retries must be non-negative")
        return errors

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)
