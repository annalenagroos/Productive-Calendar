from collections import Counter
from datetime import datetime, date

# ===================== EVENTS NACH MONAT ZÄHLEN ===================== #
def get_event_counts_by_month():
    from app import Event
    events = Event.query.all()
    month_counts = Counter()
    for event in events:
        if event.date:
            month_key = event.date.strftime("%Y-%m")
            month_counts[month_key] += 1
    return dict(month_counts)

# ===================== EVENTS NACH WOCHENTAG ZÄHLEN ===================== #
def get_event_counts_by_weekday():
    from app import Event
    events = Event.query.all()
    weekday_counts = Counter()
    for event in events:
        if event.date:
            weekday = event.date.strftime("%A")
            weekday_counts[weekday] += 1
    return dict(weekday_counts)

# ===================== AUFGABEN: ERLEDIGT VS. OFFEN ===================== #
def get_task_completion_stats():
    from app import Task
    tasks = Task.query.all()
    done = sum(1 for t in tasks if t.done)
    open_ = sum(1 for t in tasks if not t.done)
    return {'Erledigt': done, 'Offen': open_}

# ===================== EVENTS NACH TAGESZEIT CLUSTERN ===================== #
def get_event_distribution_by_time():
    from app import Event
    events = Event.query.all()
    time_clusters = {"Morgen": 0, "Mittag": 0, "Abend": 0, "Nacht": 0}

    for event in events:
        if event.date:
            hour = event.date.hour
            if 5 <= hour < 11:
                time_clusters["Morgen"] += 1
            elif 11 <= hour < 17:
                time_clusters["Mittag"] += 1
            elif 17 <= hour < 23:
                time_clusters["Abend"] += 1
            else:
                time_clusters["Nacht"] += 1
    return time_clusters

# ===================== DURCHSCHNITTLICHE ANZAHL EVENTS PRO TAG ===================== #
def get_average_events_per_day():
    from app import Event
    events = Event.query.all()
    if not events:
        return 0
    dates = [e.date.date() for e in events if e.date]
    date_range = (max(dates) - min(dates)).days + 1
    return round(len(dates) / date_range, 2) if date_range > 0 else len(dates)

# ===================== VERGANGEN VS. ZUKUNFT EVENTS ===================== #
def get_event_time_stats():
    from app import Event
    events = Event.query.all()
    now = datetime.now()
    past = sum(1 for e in events if e.date and e.date < now)
    future = sum(1 for e in events if e.date and e.date >= now)
    return {'Vergangen': past, 'Zukünftig': future}

# ===================== TOP-TAGE MIT DEN MEISTEN EVENTS ===================== #
def get_top_event_days(top_n=5):
    from app import Event
    events = Event.query.all()
    date_counts = Counter()
    for event in events:
        if event.date:
            date_key = event.date.date().isoformat()
            date_counts[date_key] += 1
    return date_counts.most_common(top_n)