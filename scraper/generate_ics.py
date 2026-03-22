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
    # ICS aus der Library generieren
    ics_text = cal.serialize()

    # Unser eigener Header, damit iOS den Kalendernamen übernimmt
    header = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Windhunde UCI Calendar 2026//EN\n"
        "X-WR-CALNAME:Windhunde UCI Calendar 2026\n"
        "X-WR-TIMEZONE:America/Los_Angeles\n"
    )

    # Das von der Library erzeugte BEGIN:VCALENDAR ersetzen
    ics_text = ics_text.replace("BEGIN:VCALENDAR", header, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(ics_text)

if __name__ == "__main__":
    with open("scraper/events.json", "r", encoding="utf-8") as f:
        events = json.load(f)

    cal = build_ics(events)
    save_ics(cal)
    print(f"Saved ICS with {len(events)} events to calendar/uci-2026.ics")
