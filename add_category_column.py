import sqlite3

def add_category_column_safely():
    conn = sqlite3.connect("instance/database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE event ADD COLUMN category TEXT")
        print("Spalte 'category' wurde hinzugefügt.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Spalte 'category' existiert bereits – kein Problem.")
        else:
            raise
    finally:
        conn.commit()
        conn.close()

# Script ausführen
add_category_column_safely()