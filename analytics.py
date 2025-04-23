from collections import Counter  # Zählt automatisch gleiche Einträge wie ein intelligenter Zähler

# ===================== EVENTS NACH MONAT ZÄHLEN ===================== #
def get_event_counts_by_month():
    from app import Event  # Lazy-Import, um zirkuläre Abhängigkeiten zu vermeiden
    events = Event.query.all()  # Alle Events aus der Datenbank abfragen

    month_counts = Counter()  # Counter zum Zählen der Events pro Monat

    for event in events:
        if event.date:  # Sicherstellen, dass ein Datum vorhanden ist
            # Erzeuge Schlüssel im Format "YYYY-MM", z. B. "2025-04"
            month_key = event.date.strftime("%Y-%m")
            month_counts[month_key] += 1  # Erhöhe Zähler für den entsprechenden Monat

    return dict(month_counts)  # Rückgabe als normales Dictionary


# ===================== EVENTS NACH WOCHENTAG ZÄHLEN ===================== #
def get_event_counts_by_weekday():
    from app import Event  # Wieder lazy import für sauberen modularen Code
    events = Event.query.all()  # Alle Events holen

    weekday_counts = Counter()  # Counter für Wochentage

    for event in events:
        if event.date:  # Prüfe auf gültiges Datum
            # Hole den vollständigen Wochentagsnamen, z. B. "Monday"
            weekday = event.date.strftime("%A")
            weekday_counts[weekday] += 1

    return dict(weekday_counts)  # Rückgabe als normales Dictionary


# ===================== AUFGABEN: ERLEDIGT VS. OFFEN ===================== #
def get_task_completion_stats():
    from app import Task  # Lazy import des Task-Modells
    tasks = Task.query.all()  # Alle Aufgaben laden

    # Anzahl der erledigten Aufgaben
    done = sum(1 for t in tasks if t.done)

    # Anzahl der offenen Aufgaben
    open_ = sum(1 for t in tasks if not t.done)

    # Rückgabe eines übersichtlichen Dictionarys
    return {
        'Erledigt': done,
        'Offen': open_
    }
