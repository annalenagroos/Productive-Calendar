import sqlite3   # Ermöglicht den Zugriff auf SQLite-Datenbanken
import os        # Ermöglicht Dateiprüfung im Dateisystem

# 🔧 Liste mit Pfaden zu Datenbankdateien, die geprüft werden sollen
db_files = [
    "calendar.db",                # Hauptdatenbank im Projektverzeichnis
    "instance/database.db",       # Zusätzliche Datenbank in Unterordner "instance"
    "instance/dashboard.db"
]

# 🔁 Schleife über jede Datenbankdatei in der Liste
for db_path in db_files:
    # ✅ Überprüfen, ob die Datei tatsächlich existiert
    if os.path.exists(db_path):
        print(f"\n🔍 Prüfe {db_path} ...")

        # 📡 Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 📋 Abfrage aller Tabellennamen aus dem internen SQLite-Metadaten-Objekt
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()  # Gibt Liste von Tupeln zurück, z.B. [('task',), ('event',)]

        # 🖨️ Ausgabe der Tabellennamen als Liste von Strings
        print(f"📋 Tabellen:", [t[0] for t in tables])

        # 🔚 Verbindung schliessen
        conn.close()
    else:
        # ❌ Wenn Datei nicht vorhanden ist, Hinweis ausgeben
        print(f"❌ Datei nicht gefunden: {db_path}")