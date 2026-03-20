from pathlib import Path
from prompt_toolkit.completion import Completer, Completion


class QuizCompleter(Completer):
    def __init__(self, quizzes_dir: Path, commands: list[str] | None = None):
        self.quizzes_dir = quizzes_dir
        self.commands = commands or []

    def get_quiz_files(self) -> list[str]:
        if not self.quizzes_dir.exists():
            return []
        return sorted(file.name for file in self.quizzes_dir.glob("*.csv"))

    def get_path_suggestions(self, fragment: str) -> list[str]:
        fragment = fragment.strip().strip('"')

        if not fragment:
            base = Path(".")
            prefix = ""
        else:
            path = Path(fragment)
            if fragment.endswith(("\\", "/")):
                base = path
                prefix = ""
            else:
                base = path.parent if path.parent != Path("") else Path(".")
                prefix = path.name

        if not base.exists() or not base.is_dir():
            return []

        suggestions = []
        for child in sorted(base.iterdir()):
            if child.name.lower().startswith(prefix.lower()):
                if child.is_dir():
                    suggestions.append(str(child) + "\\")
                elif child.suffix.lower() == ".csv":
                    suggestions.append(str(child))
        return suggestions

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        stripped = text.lstrip()

        if not stripped:
            for cmd in self.commands:
                yield Completion(cmd, start_position=0)
            return

        parts = stripped.split()

        if len(parts) == 1 and not stripped.endswith(" "):
            current = parts[0]
            for cmd in self.commands:
                if cmd.startswith(current):
                    yield Completion(cmd, start_position=-len(current))
            return

        command = parts[0]

        if command == "/start":
            if len(parts) == 1 or (len(parts) == 2 and not stripped.endswith(" ")):
                current = "" if len(parts) == 1 else parts[1]
                for quiz_name in self.get_quiz_files():
                    if quiz_name.startswith(current):
                        yield Completion(quiz_name, start_position=-len(current))
                return

            if len(parts) >= 2:
                current = ""
                if len(parts) >= 3 and not stripped.endswith(" "):
                    current = parts[2]

                for mode in ["-a", "-w"]:
                    if mode.startswith(current):
                        yield Completion(mode, start_position=-len(current))
                return

        if command == "/register":
            after_command = stripped[len("/register"):].lstrip()
            current = after_command
            for suggestion in self.get_path_suggestions(current):
                yield Completion(suggestion, start_position=-len(current))
            return