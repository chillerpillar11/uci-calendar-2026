from ics import Calendar, Event
from datetime import datetime

def convert_date(d):
    return datetime.strptime(d, "%d.%m.")

def build_ics(events):
    cal = Calendar()

    for e in events:
        ev = Event()
        ev.name = f"{e['name']} ({e['category']})"
        ev.begin = convert_date(e["start"])
        ev.make_all_day()

        # Enddatum +1 Tag (ICS‑Standard)
        end = convert_date(e["end"])
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
