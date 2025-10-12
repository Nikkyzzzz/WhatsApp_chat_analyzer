import pandas as pd
import re

file_path = "WhatsApp.txt"

with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = f.readlines()

# WhatsApp export format usually starts with "[date], [time] - [name]: message"
msg_pattern = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[APMapm]{2}\s-\s")

messages = []
current_msg = {"Date": None, "Time": None, "Name": None, "Message": ""}

for line in raw_data:
    if msg_pattern.match(line):  
        # Save previous message before starting new
        if current_msg["Date"]:
            messages.append(current_msg)
        
        # Parse new message
        try:
            date_time, content = line.split(" - ", 1)
            date, time = date_time.split(", ")
            if ": " in content:
                name, message = content.split(": ", 1)
            else:
                name, message = "System", content  # system messages
            current_msg = {
                "Date": date.strip(),
                "Time": time.strip(),
                "Name": name.strip(),
                "Message": message.strip()
            }
        except ValueError:
            continue
    else:
        # Continuation of previous (multiline message)
        current_msg["Message"] += " " + line.strip()

# Add the last message
if current_msg["Date"]:
    messages.append(current_msg)

# Create DataFrame
df = pd.DataFrame(messages, columns=["Date", "Time", "Name", "Message"])

# Clean up for Excel/CSV safety
df["Message"] = df["Message"].str.replace('"', "'", regex=False)  # replace quotes
df["Message"] = df["Message"].str.replace("\n", " ", regex=False)  # remove line breaks

# Save BOTH formats
df.to_excel("cleaned_messages.xlsx", index=False, engine="openpyxl")
df.to_csv("cleaned_messages.csv", index=False, encoding="utf-8-sig")

print("Saved as cleaned_messages.xlsx and cleaned_messages.csv successfully!")
