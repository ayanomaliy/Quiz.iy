import json
import shutil
import subprocess
import webbrowser
from urllib import request, error


class AIHelper:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
        self.tags_url = "http://localhost:11434/api/tags"

    def ask_about_question(self, question, user_question: str) -> str:
        status = self.ensure_ollama_ready()

        if status != "ready":
            return "Local AI is not available."

        prompt = self._build_prompt(question, user_question)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 350,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as response:
                body = response.read().decode("utf-8")
                parsed = json.loads(body)
                return parsed.get("response", "").strip() or "No response from AI."
        except error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            return f"AI HTTP error: {e}\n{body}"
        except error.URLError:
            return "Ollama is installed but not reachable."
        except Exception as e:
            return f"AI error: {e}"

    def ensure_ollama_ready(self) -> str:
        while True:
            if not self.is_ollama_installed():
                print("\nOllama is not installed.")
                print("Options:")
                print("  y = install Ollama now")
                print("  o = open the official download page")
                print("  n = cancel")

                choice = input("Your choice (y/o/n): ").strip().lower()

                if choice == "n":
                    return "cancelled"

                if choice == "o":
                    self.open_download_page()
                    print("Opened the Ollama download page in your browser.")
                    return "cancelled"

                if choice == "y":
                    success = self.install_with_winget()
                    if success:
                        print("\nOllama installation completed.")
                        print("Retrying setup...")
                        continue
                    else:
                        print("\nAutomatic installation failed.")
                        print("Opening the official Ollama download page instead.")
                        self.open_download_page()
                        return "cancelled"

                print("Please enter y, o, or n.")
                continue

            if not self.is_ollama_running():
                print("\nOllama is installed but not running.")
                print("Please start Ollama, then press Enter to retry.")
                print("Type n to cancel.")

                choice = input("Press Enter to retry, or n to cancel: ").strip().lower()
                if choice == "n":
                    return "cancelled"
                continue

            if not self.is_model_installed(self.model):
                print(f"\nThe model '{self.model}' is not installed.")
                choice = input(f"Download '{self.model}' now? (y/n): ").strip().lower()

                if choice != "y":
                    return "cancelled"

                success = self.pull_model(self.model)
                if success:
                    print(f"\nModel '{self.model}' installed successfully.")
                    continue
                else:
                    print(f"\nFailed to install model '{self.model}'.")
                    return "cancelled"

            return "ready"

    def is_ollama_running(self) -> bool:
        try:
            req = request.Request(self.tags_url, method="GET")
            with request.urlopen(req, timeout=3):
                return True
        except Exception:
            return False

    def is_ollama_installed(self) -> bool:
        if shutil.which("ollama") is not None:
            return True

        try:
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def is_model_installed(self, model_name: str) -> bool:
        try:
            req = request.Request(self.tags_url, method="GET")
            with request.urlopen(req, timeout=5) as response:
                body = response.read().decode("utf-8")
                parsed = json.loads(body)

            models = parsed.get("models", [])
            installed_names = {m.get("name", "") for m in models}

            return (
                model_name in installed_names
                or f"{model_name}:latest" in installed_names
            )
        except Exception:
            return False

    def install_with_winget(self) -> bool:
        try:
            result = subprocess.run(
                [
                    "winget", "install",
                    "--id", "Ollama.Ollama",
                    "-e",
                    "--accept-source-agreements",
                    "--accept-package-agreements",
                ],
                text=True,
                timeout=900,
                shell=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def pull_model(self, model_name: str) -> bool:
        try:
            result = subprocess.run(
                ["ollama", "pull", model_name],
                text=True,
                timeout=3600,
                shell=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def open_download_page(self) -> None:
        webbrowser.open("https://ollama.com/download")

    def _build_prompt(self, question, user_question: str) -> str:
        if question.qtype == "multiplechoice":
            options_text = "\n".join(
                f"{i}) {option}" for i, option in enumerate(question.options, start=1)
            )

            if len(question.correct) == 0:
                correct_text = "None of the listed options is correct."
            else:
                correct_text = ", ".join(
                    f"{i}) {question.options[int(i) - 1]}"
                    for i in sorted(question.correct, key=int)
                )

            question_info = f"""Question type: multiplechoice
Question: {question.text}
Options:
{options_text}
Correct answer(s): {correct_text}
"""
        else:
            correct_text = ", ".join(sorted(question.correct))
            question_info = f"""Question type: text
Question: {question.text}
Expected answer tokens: {correct_text}
"""

        return f"""You are an AI tutor inside a quiz app.

You are answering a follow-up question about one quiz item.

Important rules:
1. Treat the provided quiz data as ground truth.
2. First answer using the provided quiz data whenever possible.
3. You may also use general domain knowledge to explain the answer better.
4. If you use knowledge that is NOT explicitly contained in the provided quiz data, clearly label it as:
   [Additional explanation not explicitly from quiz data]
5. Never claim that something comes from the quiz if it does not.
6. If the user asks about information that would require the complete quiz set, but only one quiz item is available, say clearly:
   [Not available from the provided quiz data]
7. Be helpful and still answer as well as you can.
8. Keep the answer structured and concise.

Preferred answer structure:
- Direct answer
- [Additional explanation not explicitly from quiz data] if needed
- [Not available from the provided quiz data] if relevant

Provided quiz data:
{question_info}

User follow-up question:
{user_question}
"""