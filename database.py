import sqlite3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db():
    # Verbindung zur SQLite-Datenbank herstellen (falls sie nicht existiert, wird sie erstellt)
    conn = sqlite3.connect('calendar.db')
    
    # Erstelle einen Cursor, um mit der Datenbank zu arbeiten
    cursor = conn.cursor()
    
    # Erstelle eine Tabelle 'events', falls sie noch nicht existiert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            date TEXT, 
            description TEXT
        )
    ''')
    
    # Speichere die Änderungen und schliesse die Verbindung
    conn.commit()
    conn.close()

# Diese Funktion kannst du beim Starten deines Programms aufrufen

def add_event(title, date, description, category=None):
    conn = sqlite3.connect("instance/database.db")  # ACHTUNG: richtige DB!
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO event (title, date, description, category)
        VALUES (?, ?, ?, ?)
    ''', (title, date, description, category))

    conn.commit()
    conn.close()

def get_events():
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    
    # SQL-Befehl zum Abrufen aller Ereignisse
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()  # Alle Ereignisse abrufen
    
    # Verbindung schliessen und zurückgeben
    conn.close()
    return events

def delete_event(event_id):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    
    # SQL-Befehl zum Löschen eines Ereignisses
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    
    # Änderungen speichern und Verbindung schliessen
    conn.commit()
    conn.close()

import datetime 

def archive_event(event_id):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    
def archive_event(event_id):
    cursor.execute('''
        INSERT INTO archived_events (id, title, date, description)
        SELECT id, title, date, description FROM events WHERE id = ?
    ''', (event_id,))
    
    # Ereignis aus der ursprünglichen Tabelle löschen
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    
    # Änderungen speichern und Verbindung schliessen
    conn.commit()
    conn.close()

def archive_old_events():
    today = datetime.date.today()
    for event in get_events():
        event_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d").date()
        if event_date < today:
            archive_event(event["id"])  # Du brauchst eine archive_event(id)-Funktion


def generate_weekly_event(title, weekday, weeks=10):
    today = datetime.date.today()
    day_delta = (weekday - today.weekday()) % 7
    first_date = today + datetime.timedelta(days=day_delta)

    for i in range(weeks):
        date = first_date + datetime.timedelta(weeks=i)
        add_event(title=title, date=date.isoformat(), category="Wiederholung")

def categorize_event(title):
    keywords = {
        "Sport": ["Yoga", "Training", "Laufen"],
        "Arbeit": ["Meeting", "Projekt", "Deadline"],
        "Privat": ["Arzt", "Geburtstag", "Familie"]
    }
    for category, words in keywords.items():
        if any(word.lower() in title.lower() for word in words):
            return category
    return "Sonstiges"
