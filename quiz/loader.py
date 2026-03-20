import csv
from pathlib import Path
from quiz.models import Question, QuizSet


class QuizLoader:
    REQUIRED_FIELDS = {"type", "question", "options", "correct"}
    VALID_TYPES = {"multiplechoice", "text", "sentence"}

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
                qtype = row["type"].strip().lower()
                question_text = row["question"].strip()
                options_raw = row["options"].strip()
                correct_raw = row["correct"].strip()

                if qtype not in self.VALID_TYPES:
                    raise ValueError(
                        f"Invalid question type '{qtype}' in {quiz_name}, line {row_number}. "
                        f"Allowed: multiplechoice, text"
                    )

                if qtype == "multiplechoice":
                    options = [opt.strip() for opt in options_raw.split("|") if opt.strip()]
                    if len(options) < 2:
                        raise ValueError(
                            f"Multiple choice question in {quiz_name}, line {row_number} "
                            f"must have at least 2 options."
                        )

                    if correct_raw == "":
                        correct = set()
                    else:
                        parts = [x.strip() for x in correct_raw.split("|") if x.strip()]
                        if not all(part.isdigit() for part in parts):
                            raise ValueError(
                                f"Invalid correct-answer format in {quiz_name}, line {row_number}. "
                                f"Use numbers like 2 or 1|3|4."
                            )
                        correct = set(parts)

                    if any(int(i) < 1 or int(i) > len(options) for i in correct):
                        raise ValueError(
                            f"Correct answer index out of range in {quiz_name}, line {row_number}."
                        )

                else:  # text
                    options = []

                    if correct_raw == "":
                        raise ValueError(
                            f"Text question in {quiz_name}, line {row_number} "
                            f"must have at least one expected answer token in 'correct'."
                        )

                    correct = {
                        token.strip().lower()
                        for token in correct_raw.split("|")
                        if token.strip()
                    }

                    if not correct:
                        raise ValueError(
                            f"Text question in {quiz_name}, line {row_number} "
                            f"must have at least one expected answer token."
                        )

                qid = f"{quiz_name}::{row_number}"

                questions.append(
                    Question(
                        id=qid,
                        qtype=qtype,
                        text=question_text,
                        options=options,
                        correct=correct,
                        source_file=quiz_name,
                    )
                )

        return QuizSet(name=quiz_name, questions=questions)