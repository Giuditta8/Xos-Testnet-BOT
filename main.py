import os
import sys
from pathlib import Path

from xos_cli.ui import show_main_menu, clear_screen, pause
from xos_cli import actions

from utils import ensure_env


@ensure_env
def main() -> None:
    """Entry point for the Xos Testnet BOT launcher."""
    base_dir = Path(__file__).resolve().parent
    actions.set_base_dir(base_dir)

    while True:
        clear_screen()
        choice = show_main_menu()

        if choice == "1":
            actions.install_dependencies()
        elif choice == "2":
            actions.open_settings_menu()
        elif choice == "3":
            actions.run_bot()
        elif choice == "4":
            actions.open_readme()
        elif choice == "5":
            actions.show_about()
        elif choice == "6":
            actions.open_register_page()
        elif choice == "7":
            actions.open_github_repo()
        elif choice == "0":
            clear_screen()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        pause()


if __name__ == "__main__":
    # Ensure the script is run in a Windows-friendly way
    if os.name == "nt":
        os.system("title Xos Testnet BOT Launcher")
    main()

