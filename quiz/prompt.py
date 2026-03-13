from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from quiz.completer import QuizCompleter


class QuizPrompt:
    def __init__(self, quizzes_dir):
        self.completer = QuizCompleter(quizzes_dir)
        self.history = InMemoryHistory()

    def ask(self, message: str) -> str:
        return prompt(
            message,
            completer=self.completer,
            complete_while_typing=True,
            history=self.history,
        ).strip()