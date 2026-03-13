from dataclasses import dataclass


@dataclass
class Question:
    id: str
    qtype: str
    text: str
    options: list[str]
    correct: set[str]
    source_file: str


@dataclass
class QuizSet:
    name: str
    questions: list[Question]