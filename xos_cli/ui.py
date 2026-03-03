from __future__ import annotations

import os
from textwrap import dedent

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

LOGO = r"""/$$   /$$                           /$$$$$$$$                    /$$                           /$$           /$$$$$$$   /$$$$$$  /$$$$$$$$
| $$  / $$                          |__  $$__/                   | $$                          | $$          | $$__  $$ /$$__  $$|__  $$__/
|  $$/ $$/  /$$$$$$   /$$$$$$$         | $$  /$$$$$$   /$$$$$$$ /$$$$$$   /$$$$$$$   /$$$$$$  /$$$$$$        | $$  \ $$| $$  \ $$   | $$   
 \  $$$$/  /$$__  $$ /$$_____/         | $$ /$$__  $$ /$$_____/|_  $$_/  | $$__  $$ /$$__  $$|_  $$_/        | $$$$$$$ | $$  | $$   | $$   
  >$$  $$ | $$  \ $$|  $$$$$$          | $$| $$$$$$$$|  $$$$$$   | $$    | $$  \ $$| $$$$$$$$  | $$          | $$__  $$| $$  | $$   | $$   
 /$$/\  $$| $$  | $$ \____  $$         | $$| $$_____/ \____  $$  | $$ /$$| $$  | $$| $$_____/  | $$ /$$      | $$  \ $$| $$  | $$   | $$   
| $$  \ $$|  $$$$$$/ /$$$$$$$/         | $$|  $$$$$$$ /$$$$$$$/  |  $$$$/| $$  | $$|  $$$$$$$  |  $$$$/      | $$$$$$$/|  $$$$$$/   | $$   
|__/  |__/ \______/ |_______/          |__/ \_______/|_______/    \___/  |__/  |__/ \_______/   \___/        |_______/  \______/    |__/"""


def clear_screen() -> None:
    """Clear the CMD screen."""
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    """Wait for user to press Enter."""
    console.print()
    console.print("[bold bright_black]Press Enter to continue...[/]", end="")
    try:
        input()
    except KeyboardInterrupt:
        pass


def _render_header() -> None:
    subtitle = "[bold magenta]Xos Testnet BOT • Rich-styled terminal interface[/]"
    panel = Panel.fit(
        LOGO + "\n\n" + subtitle,
        border_style="cyan",
        title="[bold bright_cyan]Xos Testnet[/]",
        subtitle="[bold bright_black]by vonssy • launcher wrapper[/]",
    )
    console.print(panel)


def show_main_menu() -> str:
    """Draw the main menu and return the selected option."""
    clear_screen()
    _render_header()

    console.print()
    console.rule("[bold bright_white]Main Menu[/]", style="bright_black")

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        box=None,
        show_lines=False,
    )
    table.add_column("#", justify="center", width=4)
    table.add_column("Action", justify="left")
    table.add_column("Description", justify="left")

    table.add_row(
        "[bold bright_green]1[/]",
        "[bold]Install dependencies[/]",
        "Run pip install -r requirements.txt",
    )
    table.add_row(
        "[bold bright_green]2[/]",
        "[bold]Settings[/]",
        "Accounts, proxies, run options",
    )
    table.add_row(
        "[bold bright_green]3[/]",
        "[bold]Run bot[/]",
        "Launch bot.py if available",
    )
    table.add_row(
        "[bold bright_green]4[/]",
        "[bold]Open README[/]",
        "Open project README in default viewer",
    )
    table.add_row(
        "[bold bright_green]5[/]",
        "[bold]About & Donate[/]",
        "Show author and donation info",
    )
    table.add_row(
        "[bold bright_green]6[/]",
        "[bold]Register / Faucet links[/]",
        "Open Xos Testnet related pages",
    )
    table.add_row(
        "[bold bright_green]7[/]",
        "[bold]Open original GitHub repo[/]",
        "vonssy / XosTestnet-BOT",
    )
    table.add_row(
        "[bold bright_red]0[/]",
        "[bold]Exit[/]",
        "Close launcher",
    )

    console.print(table)
    console.print()
    console.print(
        dedent(
            """\
            [bright_black]Tips:[/]
            [bright_black]- Configure [bold]accounts.txt[/] and [bold]proxy.txt[/] from Settings before running the bot.[/]
            [bright_black]- Use free / private / no proxy modes like in the original README.[/]"""
        )
    )

    console.print()
    console.print("[bold bright_white]Select option[/] [bright_black](0-7)[/]: ", end="")
    try:
        return input().strip()
    except KeyboardInterrupt:
        return "0"

