import sys
from pathlib import Path
from collections import Counter

# Parse a single log line and return a dictionary
def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3)  # Split to the parts: date, time, level, message
    if len(parts) < 4:
        return None  # Skip invalid log lines if less than 4 parts
    
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3]
    }

# Load all the logs and return a list of dictionaries
def load_logs(file_path: str) -> list:
    path = Path(file_path)

    if not path.exists():
        print(f"❌ Помилка: Файл '{file_path}' не знайдено.")
        sys.exit(1)

    try:
        with path.open("r", encoding="utf-8") as f:
            logs = [parse_log_line(line) for line in f if parse_log_line(line)]
    except Exception as e:
        print(f"❌ Помилка читання файлу: {e}")
        sys.exit(1)

    return logs

# Filter the logs by level and return a list of dictionaries
def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log["level"].lower() == level.lower(), logs))

# Count the logs by level and return a dictionary using Counter from collections
def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(log["level"] for log in logs))

# Display the log counts in a formatted table increasing level width to 16
def display_log_counts(counts: dict):
    print("\nРівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level.ljust(16)} | {count}")

# Main function to run the script
def main():
    if len(sys.argv) < 2:
        print("❌ Помилка: Вкажіть шлях до файлу логів.")
        sys.exit(1)
    
    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    
    display_log_counts(counts)

    if level_filter:
        filtered_logs = filter_logs_by_level(logs, level_filter)
        print(f"\nДеталі логів для рівня '{level_filter.upper()}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

if __name__ == "__main__":
    main()
