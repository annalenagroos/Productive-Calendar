from collections import Counter

def get_event_counts_by_month():
    from app import Event  # lazy import
    events = Event.query.all()
    month_counts = Counter()
    for event in events:
        if event.date:
            month_key = event.date.strftime("%Y-%m")
            month_counts[month_key] += 1
    return dict(month_counts)

def get_event_counts_by_weekday():
    from app import Event
    events = Event.query.all()
    weekday_counts = Counter()
    for event in events:
        if event.date:
            weekday = event.date.strftime("%A")
            weekday_counts[weekday] += 1
    return dict(weekday_counts)

def get_task_completion_stats():
    from app import Task
    tasks = Task.query.all()
    done = sum(1 for t in tasks if t.done)
    open_ = sum(1 for t in tasks if not t.done)
    return {'Erledigt': done, 'Offen': open_}