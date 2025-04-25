from extensions import db
from models import Task, Event
import csv

# ====================== AUFGABEN ARCHIVIEREN ====================== #
def archive_done_tasks():
    """Archiviert (anstatt zu löschen) alle erledigten Aufgaben."""
    done_tasks = Task.query.filter_by(done=True).all()
    count = len(done_tasks)

    for task in done_tasks:
        task.is_archived = True
    db.session.commit()
    print(f"🧹 {count} erledigte Aufgaben archiviert.")


# ====================== EXPORT: NUR EVENTS ====================== #
def export_events_to_csv(path="static/export.csv"):
    """Exportiert nur Events als CSV-Datei (Basic-Version)."""
    events = Event.query.all()
    count = len(events)

    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["ID", "Titel", "Datum", "User ID"])
        for e in events:
            writer.writerow([e.id, e.title, e.date, e.user_id])

    print(f"📁 {count} Events exportiert nach '{path}'.")


# ====================== EXPORT: ALLE DATEN ====================== #
def export_all_data(user_id=None, file_path="static/full_export.csv"):
    """Exportiert Events & Tasks als CSV. Optional für bestimmten Benutzer."""
    events = Event.query.filter_by(user_id=user_id).all() if user_id else Event.query.all()
    tasks = Task.query.filter_by(user_id=user_id).all() if user_id else Task.query.all()

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Typ", "Titel/Beschreibung", "Datum/Status"])

        for event in events:
            writer.writerow(["Termin", event.title, event.date])
        for task in tasks:
            writer.writerow(["Aufgabe", task.description, "Erledigt" if task.done else "Offen"])

    print(f"📁 Export abgeschlossen: {file_path}")


# ====================== ARCHIV LEEREN ====================== #
def clear_archive():
    """Löscht alle archivierten Aufgaben und Events."""
    deleted_tasks = Task.query.filter_by(is_archived=True).delete()
    deleted_events = Event.query.filter_by(is_archived=True).delete()
    db.session.commit()
    print(f"🗑️ Archiv geleert: {deleted_tasks} Aufgaben & {deleted_events} Termine gelöscht.")


# ====================== COMMAND LINE START ====================== #
if __name__ == "__main__":
    from app import app  # App bringt bereits das initialisierte db mit

    with app.app_context():
        print("🔧 Starte Tools...\n")
        archive_done_tasks()
        export_all_data()
        # clear_archive()
        print("✅ Tools abgeschlossen.\n")
