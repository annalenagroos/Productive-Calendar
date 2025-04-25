import sqlite3

def add_column_if_not_exists(db_path, table_name, column_name, column_type):
    """
    Fügt eine Spalte zu einer Tabelle in einer SQLite-Datenbank hinzu,
    falls diese noch nicht existiert.

    :param db_path: Pfad zur SQLite-Datenbankdatei
    :param table_name: Name der Tabelle
    :param column_name: Name der neuen Spalte
    :param column_type: Datentyp der Spalte (z. B. 'BOOLEAN', 'TEXT')
    """
    # Verbindung zur Datenbank öffnen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Holen der Spalteninformationen zur Tabelle
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]  # Nur die Spaltennamen extrahieren

    # Prüfen, ob die gewünschte Spalte schon existiert
    if column_name not in columns:
        print(f"Füge Spalte '{column_name}' zur Tabelle '{table_name}' hinzu...")
        # ALTER TABLE Befehl zum Hinzufügen der Spalte
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT 0")
        conn.commit()
    else:
        print(f"✅ Spalte '{column_name}' existiert bereits.")

    # Verbindung schliessen
    conn.close()


# =============================
# Anwendung der Funktion:
# =============================

# Wir fügen die Spalte 'is_archived' vom Typ BOOLEAN zu zwei Tabellen hinzu – wenn sie fehlt

add_column_if_not_exists("instance/dashboard.db", "task", "is_archived", "BOOLEAN")
add_column_if_not_exists("instance/dashboard.db", "event", "is_archived", "BOOLEAN")
