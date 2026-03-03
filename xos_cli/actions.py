from __future__ import annotations

import json
import os
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.panel import Panel

from .ui import clear_screen

console = Console()

_BASE_DIR: Path | None = None
CONFIG_NAME = "config.json"


def set_base_dir(base_dir: Path) -> None:
    global _BASE_DIR
    _BASE_DIR = base_dir


def _require_base_dir() -> Path:
    if _BASE_DIR is None:
        raise RuntimeError("Base directory is not set. Call set_base_dir() from main.py first.")
    return _BASE_DIR


def _config_path() -> Path:
    return _require_base_dir() / CONFIG_NAME


def _load_config() -> Dict[str, Any]:
    path = _config_path()
    if not path.exists():
        return {
            "proxy_mode": "free",  # free | private | none
            "auto_rotate_invalid_proxies": True,
            "auto_checkin": True,
            "auto_draw": True,
            "auto_wrap": True,
            "auto_unwrap": False,
            "auto_swap": True,
            "auto_add_liquidity": False,
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_config(cfg: Dict[str, Any]) -> None:
    path = _config_path()
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def install_dependencies() -> None:
    """Run pip install -r requirements.txt."""
    base = _require_base_dir()
    req = base / "requirements.txt"
    if not req.exists():
        console.print(f"[bold red]requirements.txt not found in {base}[/]")
        return

    console.print("[bold bright_cyan]Installing dependencies with pip...[/]")
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(req)]
    console.print(f"[bright_black]{' '.join(cmd)}[/]")
    console.print()
    try:
        subprocess.run(cmd, check=True)
        console.print("[bold bright_green]Dependencies installed successfully.[/]")
    except subprocess.CalledProcessError as exc:
        console.print(f"[bold red]pip failed with exit code {exc.returncode}.[/]")


def _open_in_notepad(path: Path, title: str) -> None:
    console.print(f"[bold bright_cyan]Opening {title} in Notepad...[/]")
    if os.name == "nt":
        subprocess.Popen(["notepad", str(path)])
    else:
        console.print("[yellow]Notepad is Windows-only; please open the file manually.[/]")


def _ensure_file(path: Path, header_comment: str | None = None) -> None:
    if not path.exists():
        content = ""
        if header_comment:
            content = f"# {header_comment}\n"
        path.write_text(content, encoding="utf-8")


def open_settings_menu() -> None:
    """Interactive settings menu."""
    base = _require_base_dir()
    cfg = _load_config()

    while True:
        clear_screen()
        console.print(
            Panel.fit(
                "[bold bright_white]Settings[/]\n[bright_black]Configure accounts, proxies, and automatic actions.[/]",
                border_style="magenta",
            )
        )

        console.print()
        console.print("[bold]1.[/] Edit [bold]accounts.txt[/]")
        console.print("[bold]2.[/] Edit [bold]proxy.txt[/]")
        console.print(
            f"[bold]3.[/] Proxy mode: [bold cyan]{cfg.get('proxy_mode', 'free')}[/] "
            "[bright_black](free / private / none)[/]"
        )
        console.print(
            f"[bold]4.[/] Auto rotate invalid proxies: "
            f"[bold cyan]{'ON' if cfg.get('auto_rotate_invalid_proxies', True) else 'OFF'}[/]"
        )
        console.print(
            f"[bold]5.[/] Auto check-in: [bold cyan]{'ON' if cfg.get('auto_checkin', True) else 'OFF'}[/]"
        )
        console.print(
            f"[bold]6.[/] Auto draw: [bold cyan]{'ON' if cfg.get('auto_draw', True) else 'OFF'}[/]"
        )
        console.print(
            f"[bold]7.[/] Auto wrap XOS→WXOS: [bold cyan]{'ON' if cfg.get('auto_wrap', True) else 'OFF'}[/]"
        )
        console.print(
            f"[bold]8.[/] Auto unwrap WXOS→XOS: [bold cyan]{'ON' if cfg.get('auto_unwrap', False) else 'OFF'}[/]"
        )
        console.print(
            f"[bold]9.[/] Auto random swap: [bold cyan]{'ON' if cfg.get('auto_swap', True) else 'OFF'}[/]"
        )
        console.print(
            f"[bold]10.[/] Auto add liquidity: [bold cyan]{'ON' if cfg.get('auto_add_liquidity', False) else 'OFF'}[/]"
        )
        console.print("[bold]0.[/] Back to main menu")
        console.print()
        console.print("[bold bright_white]Choose option[/] [bright_black](0-10)[/]: ", end="")

        try:
            choice = input().strip()
        except KeyboardInterrupt:
            break

        if choice == "0":
            _save_config(cfg)
            break
        elif choice == "1":
            acc_path = base / "accounts.txt"
            _ensure_file(
                acc_path,
                "One private key per line, e.g.: your_private_key_1",
            )
            _open_in_notepad(acc_path, "accounts.txt")
        elif choice == "2":
            proxy_path = base / "proxy.txt"
            _ensure_file(
                proxy_path,
                "Example: ip:port or protocol://ip:port or protocol://user:pass@ip:port",
            )
            _open_in_notepad(proxy_path, "proxy.txt")
        elif choice == "3":
            console.print(
                "[bold]Enter proxy mode[/] [bright_black](free / private / none)[/]: ",
                end="",
            )
            mode = input().strip().lower()
            if mode in {"free", "private", "none"}:
                cfg["proxy_mode"] = mode
        elif choice == "4":
            cfg["auto_rotate_invalid_proxies"] = not cfg.get("auto_rotate_invalid_proxies", True)
        elif choice == "5":
            cfg["auto_checkin"] = not cfg.get("auto_checkin", True)
        elif choice == "6":
            cfg["auto_draw"] = not cfg.get("auto_draw", True)
        elif choice == "7":
            cfg["auto_wrap"] = not cfg.get("auto_wrap", True)
        elif choice == "8":
            cfg["auto_unwrap"] = not cfg.get("auto_unwrap", False)
        elif choice == "9":
            cfg["auto_swap"] = not cfg.get("auto_swap", True)
        elif choice == "10":
            cfg["auto_add_liquidity"] = not cfg.get("auto_add_liquidity", False)

        _save_config(cfg)


def run_bot() -> None:
    """Run bot.py in the same directory, if available."""
    base = _require_base_dir()
    bot_path = base / "bot.py"
    if not bot_path.exists():
        console.print("[bold red]bot.py not found in this directory.[/]")
        console.print(
            "[bright_black]Clone the original repo or place your bot.py here, "
            "then use this launcher to run it.[/]"
        )
        return

    console.print("[bold bright_cyan]Running bot.py... (Ctrl+C to stop)[/]")
    cmd = [sys.executable, str(bot_path)]
    console.print(f"[bright_black]{' '.join(cmd)}[/]")

    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Bot interrupted by user.[/]")


def open_readme() -> None:
    """Open the main README in the default app."""
    base = _require_base_dir()
    for name in ("README.md", "Readme.md", "readme.md"):
        path = base / name
        if path.exists():
            webbrowser.open(str(path))
            console.print(f"[bold bright_cyan]Opening {name}...[/]")
            return
    console.print("[bold yellow]README file not found in project directory.[/]")


def show_about() -> None:
    """Show information and donation addresses from the README."""
    text = """[bold bright_white]Xos Testnet BOT[/]

[bold]Original README highlights:[/]
- Auto get account information
- Auto run with:
  • Proxyscrape free proxy (1)
  • Private proxy (2)
  • Without proxy (3)
- Auto rotate invalid proxies (y/n)
- Auto claim check-in, perform draw, wrap / unwrap, random swap, add liquidity
- Multi accounts

[bold]Requirements:[/]
- Python 3.9+ and pip

[bold]Donate:[/]
EVM: [bright_cyan]0xe3c9ef9a39e9eb0582e5b147026cae524338521a[/]
TON: [bright_cyan]UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB[/]
SOL: [bright_cyan]E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf[/]
SUI: [bright_cyan]0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347[/]
"""
    console.print(
        Panel.fit(
            text,
            title="[bold bright_magenta]About & Donate[/]",
            border_style="bright_magenta",
        )
    )


def open_register_page() -> None:
    """Open registration and related links mentioned in the README."""
    # README just says "Register Here: Xos Testnet" without a URL,
    # so we open a generic search query for the user.
    query_url = "https://www.google.com/search?q=Xos+Testnet"
    webbrowser.open(query_url)
    console.print(
        "[bold bright_cyan]Opening browser search for 'Xos Testnet' to register, "
        "connect wallet, claim faucet, and use XOS Dex.[/]"
    )


def open_github_repo() -> None:
    """Open original GitHub repository from README."""
    url = "https://github.com/vonssy/XosTestnet-BOT"
    webbrowser.open(url)
    console.print(f"[bold bright_cyan]Opening {url} ...[/]")

