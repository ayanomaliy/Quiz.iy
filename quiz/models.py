from dataclasses import dataclass


@dataclass
class Question:
    id: str
    text: str
    options: list[str]
    correct: set[int]
    source_file: str


@dataclass
class QuizSet:
    name: str
    questions: list[Question]