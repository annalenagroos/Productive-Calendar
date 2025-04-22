import sqlite3

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

def add_event(title, date, description):
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    
    # SQL-Befehl zum Hinzufügen eines neuen Ereignisses
    cursor.execute('''
        INSERT INTO events (title, date, description)
        VALUES (?, ?, ?)
    ''', (title, date, description))
    
    # Änderungen speichern und Verbindung schliessen
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
