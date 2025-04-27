import random
import csv
from datetime import datetime, timedelta

# Settings
NUM_CALLS = 100
OUTPUT_FILE = "New_Call.csv"


phone_numbers = []
while len(phone_numbers) < random.randint(100, 1200):  # 30 unique phone numbers
    num = random.randint(2000000000, 9999999999)
    if num not in phone_numbers:
        phone_numbers.append(num)

# Call types
call_types = ["Incoming", "Outgoing", "Missed"]
call_type_weights = [0.5, 0.45, 0.05]  # Mostly incoming/outgoing, few missed

# Random timestamp generator (only in the last 7 days)
def random_timestamp():
    now = datetime.now()
    days_ago = random.randint(0, 6)  # within a week
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    random_time = now - timedelta(days=days_ago, hours=random_hour, minutes=random_minute, seconds=random_second)
    return random_time

# Random call duration generator
def random_duration(call_type):
    if call_type == "Missed":
        return 0
    return random.randint(30, 2400)  # 30 seconds to 40 mins

# Generate the call logs
call_logs = []

for _ in range(NUM_CALLS):
    caller = random.choice(phone_numbers)
    receiver = random.choice([n for n in phone_numbers if n != caller])
    call_type = random.choices(call_types, weights=call_type_weights, k=1)[0]
    timestamp = random_timestamp()
    
    log = {
        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "Caller Number": f"+1-{str(caller)[:3]}-{str(caller)[3:6]}-{str(caller)[6:]}",
        "Receiver Number": f"+1-{str(receiver)[:3]}-{str(receiver)[3:6]}-{str(receiver)[6:]}",
        "Call Type": call_type,
        "Duration (seconds)": random_duration(call_type)
    }
    call_logs.append(log)

# Sort by timestamp to simulate chronological calling
call_logs.sort(key=lambda x: x["Timestamp"])

# Save to CSV
with open(OUTPUT_FILE, "w", newline='') as csvfile:
    fieldnames = ["Timestamp", "Caller Number", "Receiver Number", "Call Type", "Duration (seconds)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for call in call_logs:
        writer.writerow(call)

print(f"✅ Generated {NUM_CALLS} highly realistic call logs into '{OUTPUT_FILE}'")
