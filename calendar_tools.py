from extensions import db           # Zugriff auf die SQLAlchemy-Datenbankinstanz
from models import Task, Event      # Datenbankmodelle für Aufgaben und Termine
import csv                          # Für den CSV-Export

# ====================== AUFGABEN ARCHIVIEREN ====================== #
def archive_done_tasks():
    """
    Archiviert alle erledigten Aufgaben.
    Die Aufgaben werden nicht gelöscht, sondern durch 'is_archived=True' als archiviert markiert.
    """
    done_tasks = Task.query.filter_by(done=True).all()  # Alle erledigten Aufgaben abrufen
    count = len(done_tasks)  # Anzahl speichern

    for task in done_tasks:
        task.is_archived = True  # Als archiviert markieren
    db.session.commit()  # Änderungen speichern
    print(f"🧹 {count} erledigte Aufgaben archiviert.")


# ====================== EXPORT: NUR EVENTS ====================== #
def export_events_to_csv(path="static/export.csv"):
    """
    Exportiert alle Termine in eine CSV-Datei (einfaches Format).
    Standardpfad: static/export.csv
    """
    events = Event.query.all()
    count = len(events)

    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["ID", "Titel", "Datum", "User ID"])  # Kopfzeile
        for e in events:
            writer.writerow([e.id, e.title, e.date, e.user_id])

    print(f"📁 {count} Events exportiert nach '{path}'.")


# ====================== EXPORT: ALLE DATEN ====================== #
def export_all_data(user_id=None, file_path="static/full_export.csv"):
    """
    Exportiert sowohl Termine als auch Aufgaben in eine CSV-Datei.
    Optional: nur Daten eines bestimmten Benutzers (via user_id).
    """
    # Benutzergefilterte oder alle Einträge laden
    events = Event.query.filter_by(user_id=user_id).all() if user_id else Event.query.all()
    tasks = Task.query.filter_by(user_id=user_id).all() if user_id else Task.query.all()

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Typ", "Titel/Beschreibung", "Datum/Status"])  # Kopfzeile

        for event in events:
            writer.writerow(["Termin", event.title, event.date])
        for task in tasks:
            writer.writerow(["Aufgabe", task.description, "Erledigt" if task.done else "Offen"])

    print(f"📁 Export abgeschlossen: {file_path}")


# ====================== ARCHIV LEEREN ====================== #
def clear_archive():
    """
    Löscht alle Aufgaben und Termine, die als archiviert markiert wurden (is_archived = True).
    """
    deleted_tasks = Task.query.filter_by(is_archived=True).delete()
    deleted_events = Event.query.filter_by(is_archived=True).delete()
    db.session.commit()
    print(f"🗑️ Archiv geleert: {deleted_tasks} Aufgaben & {deleted_events} Termine gelöscht.")


# ====================== MANUELLER START PER KONSOLE ====================== #
if __name__ == "__main__":
    from app import app  # Die Flask-App wird importiert, um Zugriff auf Kontext & DB zu bekommen

    with app.app_context():
        print("🔧 Starte Tools...\n")
        archive_done_tasks()       # Archivieren aller erledigten Aufgaben
        export_all_data()          # Export aller Daten
        # clear_archive()          # Archivierte Aufgaben & Termine löschen (bei Bedarf entkommentieren)
        print("✅ Tools abgeschlossen.\n")