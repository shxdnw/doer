import json
import subprocess
import sys
from pathlib import Path

# ===== Colors =====
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

CONFIG_PATH = Path("menu_config.json")


def load_menu(config_path: Path):
    """Load menu config from JSON file."""
    if not config_path.exists():
        print(f"{RED}[!] Config file {config_path} not found!{RESET}", file=sys.stderr)
        sys.exit(1)
    with config_path.open("r") as f:
        return json.load(f)


def display_menu(menu: dict, exit_number: int):
    """Display the menu options."""
    print(f"\n{CYAN}=== Script Wrapper Menu ==={RESET}")
    for key, item in sorted(menu.items(), key=lambda x: int(x[0])):
        print(f"{YELLOW}{key}.{RESET} {item['name']}")
    print(f"{YELLOW}{exit_number}.{RESET} Quit")  # always last option


def main():
    menu = load_menu(CONFIG_PATH)

    # Determine exit number automatically
    numeric_keys = [int(k) for k in menu.keys() if k.isdigit()]
    exit_number = max(numeric_keys, default=0) + 1

    while True:
        display_menu(menu, exit_number)
        choice = input(f"\n{CYAN}Enter your choice:{RESET} ").strip()

        if choice == str(exit_number):
            print(f"{GREEN}Exiting...{RESET}")
            break

        if choice not in menu:
            print(f"{RED}[!] Invalid choice, try again.{RESET}")
            continue

        command = menu[choice]["command"]

        try:
            print(f"\n{CYAN}[Running]{RESET} {command}\n")
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"{RED}[Error]{RESET} Command failed with exit code {e.returncode}")
        except Exception as e:
            print(f"{RED}[Error]{RESET} {e}")

        input(f"\n{YELLOW}Press Enter to continue...{RESET}")


if __name__ == "__main__":
    main()
