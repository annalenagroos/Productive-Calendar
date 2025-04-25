import calendar
from markupsafe import Markup

class EventCalendar(calendar.HTMLCalendar):
    def __init__(self, events):
        super().__init__(calendar.SUNDAY)
        self.events = self.group_by_day(events)

    def group_by_day(self, events):
        grouped = {}
        for event in events:
            if event.date:
                day = event.date.day
                grouped.setdefault(day, []).append(event)
        return grouped

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        
        cssclass = self.cssclasses[weekday]
        events = self.events.get(day, [])
        
        if events:
            cssclass += ' filled'
            event_list = "<ul>" + "".join(f"<li>{e.title}</li>" for e in events) + "</ul>"
            return f'<td class="{cssclass}"><strong>{day}</strong>{event_list}</td>'
        return f'<td class="{cssclass}">{day}</td>'
