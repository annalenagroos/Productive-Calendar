import sqlite3

def add_column_if_not_exists(db_path, table_name, column_name, column_type):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Prüfen, ob Spalte bereits existiert
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    if column_name not in columns:
        print(f"➕ Füge Spalte '{column_name}' zur Tabelle '{table_name}' hinzu...")
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT 0")
        conn.commit()
    else:
        print(f"✅ Spalte '{column_name}' existiert bereits.")

    conn.close()

# Spalten hinzufügen
add_column_if_not_exists("instance/dashboard.db", "task", "is_archived", "BOOLEAN")
add_column_if_not_exists("instance/dashboard.db", "event", "is_archived", "BOOLEAN")
