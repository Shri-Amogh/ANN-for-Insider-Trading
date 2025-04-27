import random
import csv
from datetime import datetime, timedelta

# Settings
NUM_TEXTS = 10000
OUTPUT_FILE_TEXTS = "New_text.csv"

# Reuse the same phone numbers as before or regenerate
text_numbers = []
while len(text_numbers) < random.randint(500, 1500):
    num = random.randint(2000000000, 9999999999)
    if num not in text_numbers:
        text_numbers.append(num)

# Random timestamp generator
def random_timestamp():
    now = datetime.now()
    days_ago = random.randint(0, 30)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return (now - timedelta(days=days_ago, hours=hour, minutes=minute, seconds=second))

# Text content length
def random_text_length():
    return random.randint(12, 700)  # very short to medium texts

# Generate texts
text_logs = []

for _ in range(NUM_TEXTS):
    sender = random.choice(text_numbers)
    receiver = random.choice([n for n in text_numbers if n != sender])
    timestamp = random_timestamp()
    message_length = random_text_length()
    
    log = {
        "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "Sender Number": f"+1-{str(sender)[:3]}-{str(sender)[3:6]}-{str(sender)[6:]}",
        "Receiver Number": f"+1-{str(receiver)[:3]}-{str(receiver)[3:6]}-{str(receiver)[6:]}",
        "Message Length (characters)": message_length
    }
    text_logs.append(log)

# Sort by time
text_logs.sort(key=lambda x: x["Timestamp"])

# Save to CSV
with open(OUTPUT_FILE_TEXTS, "w", newline='') as csvfile:
    fieldnames = ["Timestamp", "Sender Number", "Receiver Number", "Message Length (characters)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for text in text_logs:
        writer.writerow(text)

print(f"✅ Generated {NUM_TEXTS} realistic text messages into '{OUTPUT_FILE_TEXTS}'")
