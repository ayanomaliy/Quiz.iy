import os
import shutil
from colorama import Fore, Style, init

init(autoreset=True)


def terminal_width() -> int:
    return shutil.get_terminal_size(fallback=(100, 30)).columns


def horizontal_rule(char: str = "=") -> str:
    return char * terminal_width()


def print_separator(char: str = "=", color: str = "cyan", leading_newline: bool = True) -> None:
    line = horizontal_rule(char)

    if color == "cyan":
        line = cyan(line)
    elif color == "purple":
        line = purple(line)
    elif color == "green":
        line = green(line)
    elif color == "red":
        line = red(line)
    elif color == "yellow":
        line = yellow(line)

    if leading_newline:
        print("\n" + line)
    else:
        print(line)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


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


def get_large_logo() -> str:
    return r"""
 ________  ___  ___  ___  ________      ___      ___    ___ 
|\   __  \|\  \|\  \|\  \|\_____  \    |\  \    |\  \  /  /|
\ \  \|\  \ \  \\\  \ \  \\|___/  /|   \ \  \   \ \  \/  / /
 \ \  \\\  \ \  \\\  \ \  \   /  / /    \ \  \   \ \    / / 
  \ \  \\\  \ \  \\\  \ \  \ /  /_/__  __\ \  \   \/  /  /  
   \ \_____  \ \_______\ \__\\________\\__\ \__\__/  / /    
    \|___| \__\|_______|\|__|\|_______\|__|\|__|\___/ /     
          \|__|                                \|___|/      
""".strip("\n")


def get_small_logo() -> str:
    return "Quiz.iy"


def print_logo() -> None:
    width = terminal_width()
    large_logo = get_large_logo()
    logo_width = max(len(line) for line in large_logo.splitlines())

    print()

    if width >= logo_width + 2:
        print(purple(large_logo))
    else:
        print(purple(bold(get_small_logo())))
        print_warning("Window too narrow for full logo. Widen the terminal to see the large version.")

    print("All rights reserved by " + purple("ayanomaliy") + ".")
    print("GitHub: " + purple("https://github.com/ayanomaliy"))


def print_intro() -> None:
    print("A simple modular quiz app that lets you test yourself using custom quizzes.\n")


def print_main_menu():
    print_separator("=")
    print_title("Quiz Menu")
    print("Commands:")
    print("  /help")
    print("  /quizzes")
    print("  /register <path_to_csv>")
    print("  /create <quizname>")
    print("  /start quizname.csv -a")
    print("  /start quizname.csv -w")
    print("  /exit")
    print_separator("=", leading_newline=False)