import sqlite3
import datetime
from flask_sqlalchemy import SQLAlchemy

# Optional: Für spätere Flask-Integration (z. B. mit Flask-Migrate)
db = SQLAlchemy()

# ================================
# 🗃️ 1. Datenbankstruktur erstellen
# ================================
def create_db():
    """
    Erstellt die SQLite-Datenbank 'calendar.db' mit den Tabellen:
    - events (aktive Termine)
    - archived_events (archivierte Termine)
    """
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    # Aktive Events
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            category TEXT
        )
    ''')

    # Archivierte Events
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archived_events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            category TEXT
        )
    ''')

    conn.commit()
    conn.close()

# ================================
# ➕ 2. Neues Event hinzufügen
# ================================
def add_event(title, date, description="", category=None):
    """
    Fügt ein neues Event in die Datenbank ein.
    Die Kategorie wird automatisch erkannt, wenn sie nicht angegeben ist.
    """
    if not category:
        category = categorize_event(title)

    conn = sqlite3.connect("calendar.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO events (title, date, description, category)
        VALUES (?, ?, ?, ?)
    ''', (title, date, description, category))

    conn.commit()
    conn.close()

# ================================
# 📥 3. Alle Events abrufen
# ================================
def get_events():
    """
    Gibt alle Events (aktive) zurück als Liste von Dictionaries.
    """
    conn = sqlite3.connect('calendar.db')
    conn.row_factory = sqlite3.Row  # Zugriff per Spaltenname
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM events ORDER BY date ASC')
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

# ================================
# ❌ 4. Event löschen
# ================================
def delete_event(event_id):
    """
    Löscht ein Event anhand seiner ID.
    """
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

# ================================
# 📦 5. Einzelnes Event archivieren
# ================================
def archive_event(event_id):
    """
    Archiviert ein Event durch Verschieben in die Tabelle 'archived_events'.
    """
    conn = sqlite3.connect('calendar.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()

    if event:
        cursor.execute('''
            INSERT INTO archived_events (id, title, date, description, category)
            SELECT id, title, date, description, category FROM events WHERE id = ?
        ''', (event_id,))
        cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()

    conn.close()

# ================================
# 🕒 6. Vergangene Events archivieren
# ================================
def archive_old_events():
    """
    Archiviert automatisch alle Events, die vor dem heutigen Datum liegen.
    """
    today = datetime.date.today()
    events = get_events()

    for event in events:
        event_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d").date()
        if event_date < today:
            archive_event(event["id"])

# ================================
# 🔁 7. Wiederkehrende Events anlegen
# ================================
def generate_weekly_event(title, weekday, weeks=10):
    """
    Erstellt ein Event, das jede Woche am gleichen Wochentag stattfindet.
    z. B. generate_weekly_event("Yoga", weekday=1, weeks=5)
    """
    today = datetime.date.today()
    delta_days = (weekday - today.weekday()) % 7
    first_date = today + datetime.timedelta(days=delta_days)

    for i in range(weeks):
        date = first_date + datetime.timedelta(weeks=i)
        add_event(title=title, date=date.isoformat(), category="Wiederholung")

# ================================
# 🧠 8. Automatische Kategorisierung
# ================================
def categorize_event(title):
    """
    Gibt automatisch eine Kategorie basierend auf dem Eventtitel zurück.
    """
    keywords = {
        "Sport": ["Yoga", "Training", "Laufen"],
        "Arbeit": ["Meeting", "Projekt", "Deadline"],
        "Privat": ["Arzt", "Geburtstag", "Familie"]
    }

    for category, wordlist in keywords.items():
        if any(word.lower() in title.lower() for word in wordlist):
            return category

    return "Sonstiges"

# ================================
# ▶️ 9. Beispielhafte Ausführung
# ================================
if __name__ == "__main__":
    create_db()

    # Manuelles Beispiel-Event hinzufügen
    add_event("Yoga Training", "2025-05-01", "Morgens um 8 Uhr")

    # Wiederkehrende Events erstellen
    generate_weekly_event("Team-Meeting", weekday=2, weeks=4)

    # Archivieren, falls nötig
    archive_old_events()

    # Events anzeigen
    for e in get_events():
        print(f"{e['date']}: {e['title']} ({e['category']})")