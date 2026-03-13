import time
from colorama import Fore, Style, init

init(autoreset=True)


def cyan(text: str) -> str:
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def green(text: str) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def red(text: str) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def yellow(text: str) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

def purple(text: str) -> str:
    return f"{Fore.LIGHTMAGENTA_EX}{text}{Style.RESET_ALL}"


def bold(text: str) -> str:
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"


def print_title(title: str) -> None:
    print(cyan(bold(title)))


def print_success(text: str) -> None:
    print(green(text))


def print_error(text: str) -> None:
    print(red(text))


def print_warning(text: str) -> None:
    print(yellow(text))


def print_logo() -> None:
    logo = r"""
 ________  ___  ___  ___  ________      ___      ___    ___ 
|\   __  \|\  \|\  \|\  \|\_____  \    |\  \    |\  \  /  /|
\ \  \|\  \ \  \\\  \ \  \\|___/  /|   \ \  \   \ \  \/  / /
 \ \  \\\  \ \  \\\  \ \  \   /  / /    \ \  \   \ \    / / 
  \ \  \\\  \ \  \\\  \ \  \ /  /_/__  __\ \  \   \/  /  /  
   \ \_____  \ \_______\ \__\\________\\__\ \__\__/  / /    
    \|___| \__\|_______|\|__|\|_______\|__|\|__|\___/ /     
          \|__|                                \|___|/      
"""
    print()
    print(purple(logo))
    print("All rights reserved to " + purple("ayanomaliy") + ".")
    print("GitHub: " + purple("https://github.com/ayanomaliy"))

def print_title(title: str) -> None:
    print(bold(title))


def print_main_menu():
    print(cyan(bold("=" * 60)))
    print_title(cyan("Quiz Menu"))
    print("Commands:")
    print("  /help")
    print("  /quizzes")
    print("  /register <path_to_csv>")
    print("  /start quizname.csv -a")
    print("  /start quizname.csv -w")
    print("  /exit")
    print(cyan(bold("=" * 60)))