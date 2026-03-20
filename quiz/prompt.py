from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from quiz.completer import QuizCompleter


class QuizPrompt:
    def __init__(self, quizzes_dir):
        self.quizzes_dir = quizzes_dir
        self.history = InMemoryHistory()

        self.default_commands = [
            "/help",
            "/quizzes",
            "/register",
            "/create",
            "/start",
            "/exit",
            "/github",
        ]

    def ask(self, message: str, commands: list[str] | None = None) -> str:
        completer = QuizCompleter(
            self.quizzes_dir,
            commands=commands if commands is not None else self.default_commands,
        )

        return prompt(
            message,
            completer=completer,
            complete_while_typing=True,
            history=self.history,
        ).strip()