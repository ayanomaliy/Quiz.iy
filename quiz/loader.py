import csv
from pathlib import Path
from quiz.models import Question, QuizSet


class QuizLoader:
    REQUIRED_FIELDS = {"question", "options", "correct"}

    def __init__(self, quizzes_dir: Path):
        self.quizzes_dir = quizzes_dir
        self.quizzes_dir.mkdir(parents=True, exist_ok=True)

    def list_quizzes(self) -> list[str]:
        return sorted(file.name for file in self.quizzes_dir.glob("*.csv"))

    def load_quiz(self, quiz_name: str) -> QuizSet:
        quiz_file = self.quizzes_dir / quiz_name

        if not quiz_file.exists():
            raise FileNotFoundError(f"Quiz file '{quiz_name}' not found.")

        questions = []

        with open(quiz_file, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")

            if not reader.fieldnames or not self.REQUIRED_FIELDS.issubset(set(reader.fieldnames)):
                raise ValueError(
                    f"Invalid CSV format in '{quiz_name}'. "
                    f"Required columns: {sorted(self.REQUIRED_FIELDS)}"
                )

            for row_number, row in enumerate(reader, start=2):
                question_text = row["question"].strip()

                options = [opt.strip() for opt in row["options"].split("|") if opt.strip()]
                if len(options) < 2:
                    raise ValueError(
                        f"Question in {quiz_name}, line {row_number} must have at least 2 options."
                    )

                correct_raw = row["correct"].strip()

                if correct_raw == "":
                    correct = set()
                else:
                    try:
                        correct = {
                            int(x.strip())
                            for x in correct_raw.split("|")
                            if x.strip()
                        }
                    except ValueError:
                        raise ValueError(
                            f"Invalid correct-answer format in {quiz_name}, line {row_number}."
                        )

                if any((i < 1 or i > len(options)) for i in correct):
                    raise ValueError(
                        f"Correct answer index out of range in {quiz_name}, line {row_number}."
                    )

                qid = f"{quiz_name}::{row_number}"

                questions.append(
                    Question(
                        id=qid,
                        text=question_text,
                        options=options,
                        correct=correct,
                        source_file=quiz_name,
                    )
                )

        return QuizSet(name=quiz_name, questions=questions)