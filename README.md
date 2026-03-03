# Xos-Testnet-BOT
XOS Testnet BOT — Automation tool for XOS testnet with multi-account management, proxy support, automated daily check-in, token wrapping, DEX swapping, liquidity provision, batch operations, and Rich terminal interface for cross-chain blockchain testnet farming
<div align="center">

```
/$$   /$$                           /$$$$$$$$                    /$$                           /$$           /$$$$$$$   /$$$$$$  /$$$$$$$$
| $$  / $$                          |__  $$__/                   | $$                          | $$          | $$__  $$ /$$__  $$|__  $$__/
|  $$/ $$/  /$$$$$$   /$$$$$$$         | $$  /$$$$$$   /$$$$$$$ /$$$$$$   /$$$$$$$   /$$$$$$  /$$$$$$        | $$  \ $$| $$  \ $$   | $$   
 \  $$$$/  /$$__  $$ /$$_____/         | $$ /$$__  $$ /$$_____/|_  $$_/  | $$__  $$ /$$__  $$|_  $$_/        | $$$$$$$ | $$  | $$   | $$   
  >$$  $$ | $$  \ $$|  $$$$$$          | $$| $$$$$$$$|  $$$$$$   | $$    | $$  \ $$| $$$$$$$$  | $$          | $$__  $$| $$  | $$   | $$   
 /$$/\  $$| $$  | $$ \____  $$         | $$| $$_____/ \____  $$  | $$ /$$| $$  | $$| $$_____/  | $$ /$$      | $$  \ $$| $$  | $$   | $$   
| $$  \ $$|  $$$$$$/ /$$$$$$$/         | $$|  $$$$$$$ /$$$$$$$/  |  $$$$/| $$  | $$|  $$$$$$$  |  $$$$/      | $$$$$$$/|  $$$$$$/   | $$   
|__/  |__/ \______/ |_______/         |__/ \_______/|_______/    \___/  |__/  |__/ \_______/   \___/        |_______/  \______/    |__/
```

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![XOS](https://img.shields.io/badge/XOS-Testnet-8B5CF6?style=for-the-badge)](https://docs.x.ink/)
[![Rich](https://img.shields.io/badge/Rich-CLI-FFB86C?style=for-the-badge)](https://github.com/Textualize/rich)

**CLI tool for XOS Testnet automation — multi-account, proxy support, auto check-in, wrap, swap & liquidity**

[Features](#features) • [Getting Started](#getting-started) • [Configuration](#configuration) • [Usage](#usage) • [Project Structure](#project-structure) • [FAQ](#faq)

</div>

---

## Official Links

| Resource | URL |
|----------|-----|
| **XOS Documentation** | https://docs.x.ink/ |
| **XOS Platform** | https://platform.x.ink/ |
| **Testnet Faucet** | https://faucet.x.ink/ |
| **XOS DEX** | https://dex.x.ink/ |
| **Block Explorer** | https://testnet.xoscan.io/ |
| **Original GitHub Repo** | https://github.com/vonssy/XosTestnet-BOT |

---

## Features

<table>
<tr>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Multi-account support | ✅ |
| Free proxy (Proxyscrape) | ✅ |
| Private proxy support | ✅ |
| No-proxy mode | ✅ |
| Auto rotate invalid proxies | ✅ |
| Auto check-in | ✅ |
| Auto draw | ✅ |
| Auto wrap XOS→WXOS | ✅ |
| Auto unwrap WXOS→XOS | ✅ |
| Auto random swap | ✅ |

</td>
<td width="50%">

| Feature | Status |
|---------|:------:|
| Auto add liquidity | ✅ |
| Rich CLI interface | ✅ |
| Config persistence (config.json) | ✅ |
| accounts.txt editor | ✅ |
| proxy.txt editor | ✅ |
| pip dependency installer | ✅ |
| Windows Notepad integration | ✅ |
| Quick links (faucet, DEX, GitHub) | ✅ |

</td>
</tr>
</table>

---

## Getting Started

### Prerequisites

- **Python 3.9+** with pip
- **Windows** (recommended; Notepad integration is Windows-only)
- **bot.py** — clone from [vonssy/XosTestnet-BOT](https://github.com/vonssy/XosTestnet-BOT) or place your bot script in the project root

### Install

```bash
git clone https://github.com/vonssy/XosTestnet-BOT.git
cd XosTestnet-BOT
python main.py
```

From the main menu, choose **1** to install dependencies.

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.0.0 | Rich console output, panels, tables |

---

## Configuration

### config.json

Created automatically on first run. Example with all options:

```json
{
  "proxy_mode": "free",
  "auto_rotate_invalid_proxies": true,
  "auto_checkin": true,
  "auto_draw": true,
  "auto_wrap": true,
  "auto_unwrap": false,
  "auto_swap": true,
  "auto_add_liquidity": false
}
```

| Option | Values | Description |
|--------|--------|-------------|
| `proxy_mode` | `free` \| `private` \| `none` | Proxy source |
| `auto_rotate_invalid_proxies` | `true` \| `false` | Replace failed proxies |
| `auto_checkin` | `true` \| `false` | Auto claim daily check-in |
| `auto_draw` | `true` \| `false` | Auto perform draw |
| `auto_wrap` | `true` \| `false` | Auto wrap XOS→WXOS |
| `auto_unwrap` | `true` \| `false` | Auto unwrap WXOS→XOS |
| `auto_swap` | `true` \| `false` | Auto random swap |
| `auto_add_liquidity` | `true` \| `false` | Auto add liquidity |

### accounts.txt

One private key per line (no header):

```
0x1234567890abcdef...
0xfedcba0987654321...
```

### proxy.txt

One proxy per line. Supported formats:

```
ip:port
http://ip:port
http://user:pass@ip:port
socks5://user:pass@ip:port
```

---

## Usage

### CLI Menu

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Xos Testnet                                                                  │
│ Xos Testnet BOT • Rich-style interactive terminal                             │
│ by vonssy • automation wrapper                                               │
└─────────────────────────────────────────────────────────────────────────────┘

──────────────────────────────── Main Menu ────────────────────────────────────

  #   Action                    Description
───  ─────────────────────────  ─────────────────────────────────────────────
  1   Install dependencies       Run pip install -r requirements.txt
  2   Settings                   Accounts, proxies, run options
  3   Run bot                    Launch bot.py if available
  4   Open README                Open project README in default viewer
  5   About & Donate             Show author and donation info
  6   Register / Faucet links    Open Xos Testnet related pages
  7   Open original GitHub repo  vonssy / XosTestnet-BOT
  0   Exit                       Close launcher

Select option (0-7):
```

### Workflow

1. Run `python main.py`
2. Choose **1** to install dependencies
3. Choose **2** → edit `accounts.txt` and `proxy.txt`, configure auto-actions
4. Choose **3** to run the bot (requires `bot.py` in project root)

---

## Project Structure

```
XosTestnet-BOT/
├── main.py              # Entry point, menu loop
├── bot.py               # Core bot logic (from original repo)
├── requirements.txt     # Python dependencies
├── config.json          # Auto-generated config
├── accounts.txt         # Private keys (one per line)
├── proxy.txt            # Proxy list
├── README.md
├── tags.txt
└── xos_cli/
    ├── __init__.py
    ├── actions.py       # Install, settings, run bot, links
    └── ui.py            # Rich UI, menu, ASCII logo
```

---

## FAQ

<details>
<summary><b>Where do I get bot.py?</b></summary>

Clone the original repository: [vonssy/XosTestnet-BOT](https://github.com/vonssy/XosTestnet-BOT). The launcher expects `bot.py` in the same directory as `main.py`. If missing, option **3** will show an error and instructions.
</details>

<details>
<summary><b>What is proxy_mode?</b></summary>

- **free** — use Proxyscrape free proxies
- **private** — use proxies from `proxy.txt`
- **none** — run without proxy
</details>

<details>
<summary><b>Is XOS Testnet V1 still active?</b></summary>

According to [XOS docs](https://docs.x.ink/users/introduction/what-is-the-xos), the V1 testnet has completed and is now offline. A POW testnet is planned for a future phase. This launcher remains useful for documentation and future testnet phases.
</details>

<details>
<summary><b>How do I add XOS Testnet to MetaMask?</b></summary>

Use the official docs: [Connect to XOS](https://platform.x.ink/users/getting-started/connect-to-the-xos). Chain ID: **1267**. RPC: `https://testnet-rpc.x.ink/` or `https://testnet-rpc.xoscan.io/`.
</details>

<details>
<summary><b>Can I run this on Linux or macOS?</b></summary>

Yes. Python and Rich work cross-platform. The only limitation: option **2** (Settings) uses Windows Notepad for editing files. On Linux/macOS, you must edit `accounts.txt` and `proxy.txt` manually.
</details>

<details>
<summary><b>What is WXOS?</b></summary>

WXOS is the wrapped representation of XOS (similar to WETH/ETH). The bot can auto-wrap native XOS to WXOS and optionally unwrap back.
</details>

<details>
<summary><b>Is it safe to store private keys in accounts.txt?</b></summary>

Never commit `accounts.txt` or `proxy.txt` to version control. Add them to `.gitignore`. Use only testnet keys with no real value. For mainnet, use hardware wallets or secure key management.
</details>

---

## Disclaimer

This project is for **educational and testnet purposes only**. Use only on XOS testnet with test tokens. Do not use mainnet private keys or real funds. The authors are not responsible for any loss of funds or misuse. Always verify contracts and URLs before interacting.

---

<div align="center">

**Donate**

EVM: `0xe3c9ef9a39e9eb0582e5b147026cae524338521a`  
TON: `UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB`  
SOL: `E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf`  
SUI: `0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347`

If this project helped you, consider giving it a ⭐ on GitHub.

</div>
