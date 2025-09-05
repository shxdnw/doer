import json
import subprocess
import sys
from pathlib import Path
import os
from datetime import datetime

# ===== Colors =====
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

CONFIG_PATH = Path("menu_config.json")
LOG_PATH = Path("script_launcher.log")


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def load_menu(config_path: Path):
    """Load menu config from JSON file."""
    if not config_path.exists():
        print(f"{RED}[!] Config file not found!{RESET}")
        print(f"    Tried path: {config_path.resolve()}")
        sys.exit(1)
    with config_path.open("r") as f:
        menu = json.load(f)
    validate_menu(menu)
    return menu


def validate_menu(menu: dict):
    """Ensure each menu item has the required fields."""
    for key, item in menu.items():
        if not isinstance(item, dict):
            raise ValueError(f"Menu item {key} is not a dictionary")
        if "name" not in item or "command" not in item:
            raise ValueError(f"Menu item {key} missing 'name' or 'command'")


def display_menu(menu: dict, exit_number: int):
    """Display the menu options."""
    print(f"\n{CYAN}=== Script Launcher Menu ==={RESET}")
    for key, item in sorted(menu.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0]):
        desc = item.get("description", "")
        print(f"{YELLOW}{key}.{RESET} {item['name']} {CYAN}{desc}{RESET}")
    print(f"{YELLOW}{exit_number}.{RESET} Quit")  # always last option


def log_command(command: str):
    """Log executed commands with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a") as log:
        log.write(f"[{timestamp}] Ran: {command}\n")


def main():
    menu = load_menu(CONFIG_PATH)

    # Determine exit number automatically
    numeric_keys = [int(k) for k in menu.keys() if k.isdigit()]
    exit_number = max(numeric_keys, default=0) + 1

    while True:
        clear_screen()
        display_menu(menu, exit_number)

        try:
            choice = input(f"\n{CYAN}Enter your choice:{RESET} ").strip()
        except KeyboardInterrupt:
            print(f"\n{GREEN}Exiting...{RESET}")
            break

        if not choice:
            print(f"{RED}[!] Please enter a choice.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
            continue

        if choice == str(exit_number):
            print(f"{GREEN}Exiting...{RESET}")
            break

        if choice not in menu:
            print(f"{RED}[!] Invalid choice, try again.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
            continue

        command = menu[choice]["command"]
        try:
            print(f"\n{CYAN}[Running]{RESET} {command}\n")
            subprocess.run(command, shell=True, check=True)
            log_command(command)
        except subprocess.CalledProcessError as e:
            print(f"{RED}[Error]{RESET} Command failed with exit code {e.returncode}")
        except KeyboardInterrupt:
            print(f"{YELLOW}\n[Interrupted]{RESET} Command stopped by user")
        except Exception as e:
            print(f"{RED}[Error]{RESET} {e}")

        input(f"\n{YELLOW}Press Enter to continue...{RESET}")


if __name__ == "__main__":
    main()
