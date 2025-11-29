import csv
import os
from datetime import datetime, timedelta

def init_csv():
    if not os.path.exists("steps.csv"):
        with open("steps.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "datetime", "steps"])
init_csv()

def save_steps(user_id: int, steps: int):
    init_csv()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("steps.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, now, steps])
CSV_FILE = "steps.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def read_steps(user_id=None):
    data = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if user_id is None or row["user_id"] == str(user_id):
                dt = datetime.strptime(row["datetime"], DATE_FORMAT)
                steps = int(row["steps"])
                data.append((dt, steps))
    return data

def sum_steps_days(user_id: int, days: int) -> int:
    data = read_steps(user_id)
    now = datetime.now()
    start = now - timedelta(days=days-1)
    total = 0
    for dt, steps in data:
        if start.date() <= dt.date() <= now.date():
            total += steps
    return total

def avg_steps_days(user_id: int,days: int) -> float:
    data = read_steps(user_id)
    now = datetime.now()
    start = now - timedelta(days=days - 1)
    count = 0
    total = 0
    for dt, steps in data:
        if start.date() <= dt.date() <= now.date():
            total += steps
            count += 1
    return total / count if count > 0 else 0
