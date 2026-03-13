import json
from pathlib import Path


class ProgressStore:
    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.progress_file.exists():
            self._save({})

    def _load(self) -> dict:
        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save(self, data: dict) -> None:
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_wrong_ids(self, quiz_name: str) -> set[str]:
        data = self._load()
        return set(data.get(quiz_name, []))

    def add_wrong(self, quiz_name: str, question_id: str) -> None:
        data = self._load()
        wrong = set(data.get(quiz_name, []))
        wrong.add(question_id)
        data[quiz_name] = sorted(wrong)
        self._save(data)

    def remove_wrong(self, quiz_name: str, question_id: str) -> None:
        data = self._load()
        wrong = set(data.get(quiz_name, []))
        wrong.discard(question_id)
        data[quiz_name] = sorted(wrong)
        self._save(data)

    def has_wrong_questions(self, quiz_name: str) -> bool:
        return len(self.get_wrong_ids(quiz_name)) > 0