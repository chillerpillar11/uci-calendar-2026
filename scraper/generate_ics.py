from ics import Calendar, Event
from datetime import datetime
import json

def convert_date(d):
    # Jahr fix auf 2026 setzen
    return datetime.strptime(d + "2026", "%d.%m.%Y")

def build_ics(events):
    cal = Calendar()

    for e in events:
        ev = Event()
        ev.name = f"{e['name']} ({e['category']})"
        ev.begin = convert_date(e["start"])
        ev.make_all_day()

        end = convert_date(e["end"])
        # Enddatum +1 Tag (ICS-Standard: exklusiv)
        ev.end = end.replace(hour=0)

        ev.description = (
            f"Sieger 2025: {e['winner']}\n"
            f"Kategorie: {e['category']}\n"
            f"Tags: {' '.join(e['tags'])}"
        )

        cal.events.add(ev)

    return cal

def save_ics(cal, path="calendar/uci-2026.ics"):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cal)

if __name__ == "__main__":
    with open("scraper/events.json", "r", encoding="utf-8") as f:
        events = json.load(f)

    cal = build_ics(events)
    save_ics(cal)
    print(f"Saved ICS with {len(events)} events to calendar/uci-2026.ics")
