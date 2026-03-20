
# Quiz.iy

Quiz.iy is a modular terminal-based quiz application for learning with custom CSV quizzes.

You can:

- create quizzes directly inside the program
- register existing quiz CSV files
- practice all questions or only previously wrong ones
- use different question types
- optionally ask local AI follow-up questions after a quiz question

It is designed both as a usable end-user tool and as an open-source Python project that can be extended.

---

## Download

### Windows

[Download the latest Windows installer](https://github.com/ayanomaliy/Quiz.iy/releases/latest/download/Quiz.iy-Setup.exe)

The installer places the program in a user-writable folder by default so the application can store quizzes and progress without permission issues.

---

## Features

- terminal-based interactive quiz app
- custom quizzes stored as CSV files
- interactive quiz creator with `/create`
- progress tracking for wrong answers
- practice mode for wrong questions only
- support for multiple question types
- tab-completion for commands
- colored terminal UI
- optional local AI follow-up support
- open-source and easy to extend

---

## Quick Start

After installation, launch **Quiz.iy** and use commands like:

```text
/help
/quizzes
/create my_quiz
/start my_quiz.csv -a
````

A typical first workflow is:

1. Create a quiz with `/create my_quiz`
2. Start it with `/start my_quiz.csv -a`
3. Review wrong questions later with `/start my_quiz.csv -w`

---

## Commands

Inside the program you can use:

```text
/help
/quizzes
/register <path_to_csv>
/create <quizname>
/start quizname.csv -a
/start quizname.csv -w
/exit
```

### Command overview

`/help`
Show the help text.

`/quizzes`
List all available registered quiz files.

`/register <path_to_csv>`
Copy an existing CSV quiz file into the program.

`/create <quizname>`
Create a new quiz interactively.

`/start quizname.csv -a`
Start a quiz with all questions.

`/start quizname.csv -w`
Start a quiz using only previously wrong questions.

`/exit`
Exit the program.

---

## Quiz Modes

### All questions

```text
/start quizname.csv -a
```

Asks every question in the quiz.

### Wrong questions only

```text
/start quizname.csv -w
```

Only asks questions that were answered incorrectly before.

---

## CSV Quiz Format

Quizzes are stored as `.csv` files using this format:

```text
type;question;options;correct
```

### Columns

| Column     | Description                             |                    |
| ---------- | --------------------------------------- | ------------------ |
| `type`     | `multiplechoice`, `text`, or `sentence` |                    |
| `question` | the question text                       |                    |
| `options`  | answer options separated by `           | ` where applicable |
| `correct`  | the correct answer or answers           |                    |

---

## Question Types

### 1. Multiple choice

Example:

```text
multiplechoice;What is the capital of France?;Berlin|Madrid|Paris|Rome;3
```

Multiple correct answers:

```text
multiplechoice;Which are programming languages?;Python|Banana|Java|Table|C++;1|3|5
```

If none of the answers are correct, leave `correct` empty:

```text
multiplechoice;Which number is greater than 10?;1|2|3|4;
```

### 2. Text

Text questions require the user to type the answer.

Example:

```text
text;Give the irregular verb forms of "go";;go|went|gone
```

Accepted input:

```text
go went gone
```

Order does not matter:

```text
went gone go
```

Both are accepted.

### 3. Sentence

Sentence questions are checked more loosely than exact text questions.
They are useful when the answer should contain specific words or ideas instead of matching a strict sequence exactly.

Example:

```text
sentence;Explain what photosynthesis does;;plants convert light energy into chemical energy
```

---

## Creating a Quiz Inside the Program

You can create quizzes interactively:

```text
/create english_verbs
```

The program will guide you through the quiz creation process and save the file automatically.

---

## Local AI Follow-Up Support (Optional)

Quiz.iy can optionally support local AI follow-up questions after quiz questions.

This feature is intended for things like:

* asking why an answer was wrong
* requesting an explanation of a concept
* getting extra learning context

The project uses a local Ollama-based integration for this feature.

If Ollama is not installed or configured, the main quiz functionality still works normally.

---

## Running from Source

### Requirements

* Python 3
* `prompt_toolkit`
* optionally `ollama` for local AI integration

Install dependencies:

```bash
pip install prompt_toolkit ollama
```

Then run:

```bash
python main.py
```

---

## Building the Windows Executable

The project can be packaged into a standalone Windows executable using PyInstaller.

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build the executable

Run this in the project folder:

```bash
py -m PyInstaller --onefile --name quiziy main.py
```

The executable will be created in:

```text
dist/quiziy.exe
```

---

## Building the Windows Installer

The project can also be packaged as a Windows installer using Inno Setup.

Typical workflow:

1. Build the executable with PyInstaller
2. Compile the `installer.iss` script with Inno Setup
3. Upload the generated `Quiz.iy-Setup.exe` to GitHub Releases

If Inno Setup is installed, you can compile from the command line:

```bat
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

The installer output will be written to:

```text
installer-output/Quiz.iy-Setup.exe
```

---

## Project Structure

A rough overview of the codebase:

```text
main.py        - application entry point
commands.py    - command parsing
prompt.py      - interactive command prompt
completer.py   - tab completion
loader.py      - CSV quiz loading
models.py      - question data structures
engine.py      - quiz execution logic
creator.py     - interactive quiz creation
storage.py     - persistence for wrong-answer tracking
ui.py          - terminal formatting / UI helpers
help_text.py   - built-in help text
ai_helper.py   - optional Ollama integration
```

---

## Extending the Project

Quiz.iy is structured so new features can be added without rewriting the whole app.

Examples of possible extensions:

* new question types
* scoring/statistics
* import/export tools
* better review modes
* categories or tags
* improved AI tutoring support
* richer terminal UI
* GUI frontend in the future

If you want to add a new question type, the main places to inspect are:

* `models.py`
* `loader.py`
* `engine.py`
* `creator.py`

---

## Notes

* The Windows installer should not install the app into `Program Files`, because Quiz.iy needs write access to its own folder during normal use.
* The application is open source, so you can inspect, modify, and extend it freely.
* The released Windows installer is currently the easiest way for non-technical users to run the program.

---

## Author

Created by **ayanomaliy**

GitHub:
[https://github.com/ayanomaliy](https://github.com/ayanomaliy)

```
```
