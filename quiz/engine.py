import random
from quiz.models import QuizSet, Question
from quiz.storage import ProgressStore
from quiz.ui import print_success, print_error, print_warning, cyan, bold


class QuizEngine:
    def __init__(self, progress_store: ProgressStore):
        self.progress_store = progress_store

    def run_quiz(self, quiz: QuizSet, mode: str) -> None:
        wrong_ids = self.progress_store.get_wrong_ids(quiz.name)

        if mode == "-w":
            selected_questions = [q for q in quiz.questions if q.id in wrong_ids]
            if not selected_questions:
                print_warning("\nThere are no wrong questions saved for this quiz.")
                return
        else:
            selected_questions = quiz.questions[:]

        random.shuffle(selected_questions)

        correct_count = 0
        asked_count = 0

        print(cyan(bold(f"\nStarting quiz: {quiz.name}")))
        print("Use /quit to return to the main menu.\n")

        for question in selected_questions:
            result = self.ask_question(question)

            if result == "quit":
                print("\nReturning to main menu.")
                return

            asked_count += 1

            if result == question.correct:
                if question.qtype == "multiplechoice" and len(question.correct) == 0:
                    print_success("Correct! Indeed, none of the answers is correct.\n")
                else:
                    print_success("Correct!\n")
                correct_count += 1
                self.progress_store.remove_wrong(quiz.name, question.id)
            else:
                if question.qtype == "multiplechoice":
                    if len(question.correct) == 0:
                        print_error("Wrong! The correct answer was: none of the above.\n")
                    else:
                        correct_text = ", ".join(
                            f"{i}) {question.options[int(i) - 1]}"
                            for i in sorted(question.correct, key=int)
                        )
                        print_error(f"Wrong! Correct answer(s): {correct_text}\n")
                else:
                    correct_text = " ".join(sorted(question.correct))
                    print_error(f"Wrong! Expected answer tokens: {correct_text}\n")

                self.progress_store.add_wrong(quiz.name, question.id)

        print(cyan("=" * 50))
        print(cyan(bold(f"Quiz finished: {quiz.name}")))
        print(f"Correctly answered: {correct_count}/{asked_count}")
        print(f"Still saved as wrong: {len(self.progress_store.get_wrong_ids(quiz.name))}")
        print(cyan("=" * 50))

    def ask_question(self, question: Question):
        print(cyan("-" * 50))
        print(cyan(bold(f"Question: {question.text}\n")))

        if question.qtype == "multiplechoice":
            for i, option in enumerate(question.options, start=1):
                print(f"{i}) {option}")

            if len(question.correct) == 0:
                print("\nNone of the listed answers is correct.")
                print("Press Enter without typing anything if you think that is correct.")
            elif len(question.correct) == 1:
                print("\nEnter one answer number.")
            else:
                print("\nEnter all correct answer numbers separated by spaces.")
                print("Example: 1 3 5")

        else:
            print("Type your answer words separated by spaces.")
            print("Word order does not matter.")
            print("Example: go went gone")

        while True:
            user_input = input("\nYour answer: ").strip()

            if user_input == "/quit":
                return "quit"

            parsed = self.parse_answer(user_input, question.qtype)
            if parsed is not None:
                return parsed

            if question.qtype == "multiplechoice":
                if len(question.correct) == 0:
                    print_warning("Invalid input. Press Enter for 'none correct', or use /quit.")
                else:
                    print_warning("Invalid input. Please enter answer numbers like: 2 or 1 3 5")
            else:
                print_warning("Invalid input. Please enter words separated by spaces.")

    def parse_answer(self, user_input: str, qtype: str):
        if qtype == "multiplechoice":
            if user_input == "":
                return set()

            normalized = user_input.replace(",", " ")
            parts = [p for p in normalized.split() if p]

            if not parts:
                return set()

            if not all(part.isdigit() for part in parts):
                return None

            return set(parts)

        else:  # text
            if user_input == "":
                return set()

            normalized = user_input.replace(",", " ")
            parts = [p.strip().lower() for p in normalized.split() if p.strip()]

            if not parts:
                return set()

            return set(parts)