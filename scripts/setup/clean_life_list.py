import csv
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
input_file = os.path.join(base_dir, "data/life_list.csv")
output_file = os.path.join(base_dir, "data/life_list_cleaned.csv")

with open(input_file, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

rows = []
i = 0
while i + 3 < len(lines):
    name = lines[i]
    date = lines[i + 1]
    location = lines[i + 2]
    region = lines[i + 3]
    rows.append([name, date, location, region])
    i += 4

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["common_name", "first_observation", "location", "region"])
    writer.writerows(rows)

print(f"Cleaned CSV written to {output_file}")