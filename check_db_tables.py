import sqlite3
import os

db_files = [
    "calendar.db",
    "instance/database.db",
    "instance/dashboard.db"
]

for db_path in db_files:
    if os.path.exists(db_path):
        print(f"\n🔍 Prüfe {db_path} ...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tabellen:", [t[0] for t in tables])
        conn.close()
    else:
        print(f"❌ Datei nicht gefunden: {db_path}")
