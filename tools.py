from app import app, db, Task, Event
import csv
from datetime import datetime

def archive_done_tasks():
    """Archiviert (löscht) alle erledigten Aufgaben."""
    done_tasks = Task.query.filter_by(done=True).all()
    count = len(done_tasks)

    for task in done_tasks:
        task.is_archived = True  # 🟩 Alternative zu Löschen
        # db.session.delete(task)  ← falls du sie stattdessen löschen willst

    db.session.commit()
    print(f"🧹 {count} erledigte Aufgaben archiviert.")


def export_events_to_csv(path="static/export.csv"):
    """Exportiert alle Events als CSV-Datei."""
    events = Event.query.all()
    count = len(events)

    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["ID", "Titel", "Datum", "User ID"])
        for e in events:
            writer.writerow([e.id, e.title, e.date, e.user_id])

    print(f"📁 {count} Events exportiert nach '{path}'.")


def clear_archive():
    """Löscht alle archivierten Aufgaben und Events."""
    deleted_tasks = Task.query.filter_by(is_archived=True).delete()
    deleted_events = Event.query.filter_by(is_archived=True).delete()
    db.session.commit()
    print(f"🗑️ Archiv geleert: {deleted_tasks} Aufgaben & {deleted_events} Termine gelöscht.")


# ------------------- Wenn direkt ausgeführt -------------------
if __name__ == "__main__":
    with app.app_context():
        print("🔧 Starte Tools...\n")
        archive_done_tasks()
        export_events_to_csv()
        # clear_archive()  ← optional aktivieren
        print("\n✅ Alle Tools ausgeführt.")