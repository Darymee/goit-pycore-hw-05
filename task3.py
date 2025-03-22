import sys
from colorama import Fore, init


init(autoreset=True)

def parse_log_line(line: str) -> dict:
    try:
        parts = line.split(" ", 3)
        date = parts[0]
        time = parts[1]
        level = parts[2]
        message = parts[3] if len(parts) > 3 else ""
        return {"date": date, "time": time, "level": level, "message": message}

    except IndexError:
        print(f"Invalid line format: {line}")


def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, encoding="utf-8") as file:
            for line in file:
                logs.append(parse_log_line(line.strip()))
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Can't read file: {e}")
        sys.exit(1)
    return logs


def count_logs_by_level(logs: list) -> dict:
    counts = {"INFO": 0, "DEBUG": 0, "ERROR": 0, "WARNING": 0}
    for log in logs:
        level = log["level"].upper()
        if level in counts:
            counts[level] += 1
    return counts


def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log["level"].lower() == level.lower()]



level_colors = {
    "INFO": Fore.BLUE,
    "DEBUG": Fore.GREEN,
    "ERROR": Fore.RED,
    "WARNING": Fore.YELLOW,
    }


def display_log_counts(counts: dict):
    print("Log level | Count")
    print("----------|----------")
    for level, count in counts.items():

        color = level_colors.get(level, Fore.RESET)

        print(f"{color + level:<14}{Fore.RESET} | {count}")


def display_logs_for_level(logs: list, level: str):
    print(f"\n '{level.upper()}' details:")
    filtered_logs = filter_logs_by_level(logs, level)
    for log in filtered_logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    if len(sys.argv) < 2:
        print("Please enter the path")
        sys.exit(1)

    log_file_path = sys.argv[1]
    logs = load_logs(log_file_path)

    level_filter = None
    if len(sys.argv) > 2:
        level_filter = sys.argv[2].lower()
        if level_filter not in ["info", "debug", "error", "warning"]:
            print(f"Invalid log level '{level_filter}'.")
            sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_filter:
        display_logs_for_level(logs, level_filter)


if __name__ == "__main__":
    main()
