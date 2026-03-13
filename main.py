from pathlib import Path
import sys
import shutil

from quiz.loader import QuizLoader
from quiz.storage import ProgressStore
from quiz.engine import QuizEngine
from quiz.commands import parse_command
from quiz.help_text import get_help_text
from quiz.ui import (
    print_main_menu,
    print_logo,
    print_error,
    print_success,
    print_warning,
    print_title,
)

from quiz.prompt import QuizPrompt
from quiz.creator import QuizCreator


def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()
QUIZZES_DIR = BASE_DIR / "quizzes"
PROGRESS_FILE = BASE_DIR / "progress" / "wrong_questions.json"


def register_quiz(csv_path_str: str) -> None:
    source_path = Path(csv_path_str.strip().strip('"')).expanduser()

    if not source_path.exists():
        print_error(f"\nError: file not found: {source_path}")
        return

    if not source_path.is_file():
        print_error(f"\nError: this is not a file: {source_path}")
        return

    if source_path.suffix.lower() != ".csv":
        print_error("\nError: only .csv files can be registered.")
        return

    QUIZZES_DIR.mkdir(parents=True, exist_ok=True)
    destination = QUIZZES_DIR / source_path.name

    if destination.exists():
        answer = input(
            f"\n'{source_path.name}' already exists. Overwrite it? (y/n): "
        ).strip().lower()
        if answer != "y":
            print_warning("Registration cancelled.")
            return

    try:
        shutil.copy2(source_path, destination)
        print_success(f"\nQuiz registered: {source_path.name}")
        print(f"Saved to: {destination}")
    except Exception as e:
        print_error(f"\nError while copying file: {e}")


def print_quizzes(loader: QuizLoader, store: ProgressStore):
    quizzes = loader.list_quizzes()

    if not quizzes:
        print_warning("\nNo quiz files found in the 'quizzes' folder.")
        return

    print()
    print_title("Available Quiz Sets")
    for quiz_name in quizzes:
        wrong_count = len(store.get_wrong_ids(quiz_name))
        print(f"- {quiz_name} (wrong saved: {wrong_count})")


def main():
    loader = QuizLoader(QUIZZES_DIR)
    store = ProgressStore(PROGRESS_FILE)
    engine = QuizEngine(store)
    quiz_prompt = QuizPrompt(QUIZZES_DIR)
    creator = QuizCreator(QUIZZES_DIR)

    print_logo()
    print("A simple modular quiz app that lets you test yourself using custom quizzes.\n")

    while True:
        print_main_menu()
        user_input = quiz_prompt.ask("\nCommand: ")

        if user_input == "/exit":
            print("Program closed.")
            break

        command_type, payload = parse_command(user_input)

        if command_type == "help":
            print("\n" + get_help_text())

        elif command_type == "quizzes":
            print_quizzes(loader, store)

        elif command_type == "register":
            register_quiz(payload["path"])

        elif command_type == "create":
            created_name = creator.create_quiz_interactive(payload["quiz_name"])
            if created_name:
                print_success(f"\nQuiz created successfully: {created_name}")

        elif command_type == "start":
            quiz_name = payload["quiz_name"]
            mode = payload["mode"]

            try:
                quiz = loader.load_quiz(quiz_name)
            except Exception as e:
                print_error(f"\nError: {e}")
                continue

            if mode == "-w" and not store.has_wrong_questions(quiz_name):
                print_warning("\nThere are no wrong questions saved for this quiz.")
                print("Please choose something else.")
                continue

            engine.run_quiz(quiz, mode)

        else:
            print_error(f"\nError: {payload}")

if __name__ == "__main__":
    main()