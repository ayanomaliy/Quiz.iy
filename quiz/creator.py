import csv
from pathlib import Path


class QuizCreator:
    HEADER = ["type", "question", "options", "correct"]

    def __init__(self, quizzes_dir: Path):
        self.quizzes_dir = quizzes_dir
        self.quizzes_dir.mkdir(parents=True, exist_ok=True)

    def create_quiz_interactive(self, quiz_name: str) -> str:
        filename = quiz_name if quiz_name.lower().endswith(".csv") else f"{quiz_name}.csv"
        quiz_path = self.quizzes_dir / filename

        if quiz_path.exists():
            answer = input(f"'{filename}' already exists. Overwrite it? (y/n): ").strip().lower()
            if answer != "y":
                print("Quiz creation cancelled.")
                return ""

        rows = []

        print("\nCreating a new quiz.")
        print("Type /done at any main prompt to finish creating the quiz.\n")

        while True:
            qtype = self._ask_question_type()
            if qtype == "/done":
                break

            question = input("Enter the question: ").strip()
            if question == "/done":
                break

            if qtype == "multiplechoice":
                row = self._create_multiplechoice_row(question)
            else:
                row = self._create_text_row(question)

            rows.append(row)
            print("Question added.\n")

        with open(quiz_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(self.HEADER)
            writer.writerows(rows)

        return filename

    def _ask_question_type(self):
        while True:
            print("Select question type:")
            print("1) multiplechoice")
            print("2) text")
            choice = input("Your choice: ").strip()

            if choice == "/done":
                return "/done"
            if choice == "1":
                return "multiplechoice"
            if choice == "2":
                return "text"

            print("Invalid choice. Please enter 1, 2, or /done.\n")

    def _create_multiplechoice_row(self, question: str):
        print("\nEnter answer options one by one.")
        print("Type /done when you have entered all options.")
        print("You need at least 2 options.\n")

        options = []
        while True:
            option = input(f"Option {len(options) + 1}: ").strip()

            if option == "/done":
                if len(options) < 2:
                    print("You need at least 2 options.")
                    continue
                break

            if not option:
                print("Option cannot be empty.")
                continue

            options.append(option)

        print("\nNow enter the correct answer numbers.")
        print("Examples:")
        print("  2")
        print("  1 3 5")
        print("Press Enter if none of the options is correct.")

        while True:
            correct_input = input("Correct answer numbers: ").strip()

            if correct_input == "":
                correct = ""
                break

            normalized = correct_input.replace(",", " ")
            parts = [p for p in normalized.split() if p]

            if not parts or not all(part.isdigit() for part in parts):
                print("Please enter only answer numbers separated by spaces, or press Enter.")
                continue

            nums = [int(part) for part in parts]
            if any(n < 1 or n > len(options) for n in nums):
                print(f"Numbers must be between 1 and {len(options)}.")
                continue

            correct = "|".join(str(n) for n in sorted(set(nums)))
            break

        return [
            "multiplechoice",
            question,
            "|".join(options),
            correct,
        ]

    def _create_text_row(self, question: str):
        print("\nEnter the expected answer words/tokens.")
        print("Word order will not matter in the quiz.")
        print("Example for irregular verbs: go, went, gone")
        print("Type the tokens separated by spaces.\n")

        while True:
            answer_input = input("Expected answer tokens: ").strip()

            if not answer_input:
                print("A text question needs at least one expected answer token.")
                continue

            tokens = [token.strip().lower() for token in answer_input.replace(",", " ").split() if token.strip()]
            if not tokens:
                print("A text question needs at least one expected answer token.")
                continue

            correct = "|".join(dict.fromkeys(tokens))
            break

        return [
            "text",
            question,
            "",
            correct,
        ]