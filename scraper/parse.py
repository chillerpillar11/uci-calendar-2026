import re
import json

def parse_line(line):
    # abgesagte Rennen markieren
    cancelled = "(abgesagt)" in line or "(abgebrochen)" in line

    # Datum extrahieren
    date_match = re.search(r"\d{2}\.\d{2}\.-\d{2}\.\d{2}\.|\d{2}\.\d{2}\.", line)
    if not date_match:
        return None

    date_str = date_match.group()
    parts = date_str.split("-")

    if len(parts) == 2:
        start = parts[0]
        end = parts[1]
    else:
        start = parts[0]
        end = parts[0]

    # restliche Felder extrahieren
    fields = line[date_match.end():].split()
    if len(fields) < 3:
        return None

    name = " ".join(fields[:-3])
    category = fields[-3]
    winner = fields[-2]

    # Tags
    tags = []
    if "UWT" in category:
        tags.append("#WorldTour")
    if "Pro" in category:
        tags.append("#ProSeries")
    if category.endswith(".1") or category.endswith(".2"):
        tags.append("#UCI")

    if "-" in date_str:
        tags.append("#StageRace")
    else:
        tags.append("#OneDay")

    if cancelled:
        tags.append("#Cancelled")

    return {
        "start": start,
        "end": end,
        "name": name.strip(),
        "category": category,
        "winner": winner,
        "tags": tags,
        "cancelled": cancelled
    }

# -----------------------------
# Hauptprogramm
# -----------------------------
if __name__ == "__main__":
    with open("scraper/raw.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    events = []
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            events.append(parsed)

    with open("scraper/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    print(f"Parsed {len(events)} events.")
