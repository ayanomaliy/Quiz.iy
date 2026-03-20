
# Quiz.iy

A simple modular terminal quiz application that lets you test yourself using **custom quizzes stored as CSV files**.

You can create quizzes, register existing quiz files, and practice them directly in the terminal.

The program supports:

* Multiple choice questions
* Text questions
* Multiple correct answers
* Questions where **none of the answers is correct**
* Order-independent text answers
* Tracking previously wrong questions for targeted practice

---

## Download

[Download for Windows](https://github.com/ayanomaliy/Quiz.iy/blob/main/installer-output/Quiz.iy-Setup.exe)

# Features

* Custom quizzes stored as CSV files
* Interactive quiz creator (`/create`)
* Multiple quiz modes
* Colored terminal interface
* Tab-completion for commands
* Progress tracking of wrong answers
* Cross-platform Python application
* Can be packaged into a standalone `.exe`

---

# Commands

Inside the program you can use:

```
/help
/quizzes
/register <path_to_csv>
/create <quizname>
/start quizname.csv -a
/start quizname.csv -w
/exit
```

### Explanation

`/help`
Show help information.

`/quizzes`
List all available quiz files.

`/register <path_to_csv>`
Copy an existing CSV quiz file into the program.

`/create <quizname>`
Create a new quiz interactively.

`/start quizname.csv -a`
Start a quiz and ask **all questions**.

`/start quizname.csv -w`
Start a quiz and ask **only previously wrong questions**.

`/exit`
Exit the program.

---

# Quiz Modes

### All questions

```
/start quizname.csv -a
```

Asks every question in the quiz.

### Wrong questions only

```
/start quizname.csv -w
```

Only asks questions you previously answered incorrectly.

---

# CSV Quiz Format

Quizzes are stored as `.csv` files using this format:

```
type;question;options;correct
```

### Columns

| Column   | Description                   |   |
| -------- | ----------------------------- | - |
| type     | `multiplechoice` or `text`    |   |
| question | the question text             |   |
| options  | answer options separated by ` | ` |
| correct  | correct answers               |   |

---

# Multiple Choice Questions

Example:

```
multiplechoice;What is the capital of France?;Berlin|Madrid|Paris|Rome;3
```

Multiple correct answers:

```
multiplechoice;Which are programming languages?;Python|Banana|Java|Table|C++;1|3|5
```

If **none of the answers are correct**, leave `correct` empty:

```
multiplechoice;Which number is greater than 10?;1|2|3|4;
```

During the quiz you simply press **Enter**.

---

# Text Questions

Text questions require the user to **type the correct answer**.

Example:

```
text;Give the irregular verb forms of "go" in English;;go|went|gone
```

User input:

```
go went gone
```

Order does **not matter**:

```
went gone go
```

Both are accepted.

---

# Creating a Quiz Inside the Program

You can create quizzes interactively:

```
/create english_verbs
```

The program will ask:

* question type
* question text
* answer options
* correct answers

The quiz will automatically be saved to:

```
quizzes/english_verbs.csv
```

---

# Building the Executable (.exe)

The program can be packaged into a standalone Windows executable.

### Install PyInstaller

```
pip install pyinstaller
```

### Build the executable

Run this command inside the project folder:

```
py -m PyInstaller --onefile --name quiziy main.py
```

The executable will be created in:

```
dist/quiziy.exe
```

You can then distribute **only this file**.

When the program runs it will automatically create the necessary folders.

---

# Running the Program

From Python:

```
python main.py
```

Or using the compiled executable:

```
quiziy.exe
```

---

# Author

Created by **ayanomaliy**

GitHub:
[https://github.com/ayanomaliy](https://github.com/ayanomaliy)

