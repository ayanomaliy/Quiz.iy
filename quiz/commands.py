def parse_command(user_input: str):
    parts = user_input.strip().split(maxsplit=1)

    if not parts or not parts[0]:
        return ("invalid", "Unknown command. Type /help for help.")

    command = parts[0]

    if command == "/help":
        return ("help", None)

    if command == "/quizzes":
        return ("quizzes", None)

    if command == "/register":
        if len(parts) != 2:
            return ("invalid", "Usage: /register <path_to_csv>")
        return ("register", {"path": parts[1].strip()})

    if command == "/start":
        start_parts = user_input.strip().split()
        if len(start_parts) != 3:
            return ("invalid", "Usage: /start quizname.csv -a|-w")

        quiz_name = start_parts[1]
        mode = start_parts[2]

        if mode not in {"-a", "-w"}:
            return ("invalid", "Usage: /start quizname.csv -a|-w")

        return ("start", {"quiz_name": quiz_name, "mode": mode})

    return ("invalid", "Unknown command. Type /help for help.")