import calendar                     # Standardmodul für Kalenderfunktionen
from markupsafe import Markup       # Zum sicheren Einfügen von HTML in Templates (z. B. Jinja2)

class EventCalendar(calendar.HTMLCalendar):
    """
    Ein HTML-Kalender, der Event-Objekte anzeigt.
    Erbt von Python's calendar.HTMLCalendar.
    """

    def __init__(self, events):
        # Initialisiert den Kalender mit Sonntag als Wochenanfang
        super().__init__(calendar.SUNDAY)
        self.events = self.group_by_day(events)  # Events werden nach Tagen gruppiert

    def group_by_day(self, events):
        """
        Gruppiert eine Liste von Event-Objekten nach dem Tag (1–31).
        :param events: Liste von Event-Objekten (mit .date und .title)
        :return: dict: { tag: [event1, event2, ...], ... }
        """
        grouped = {}
        for event in events:
            if event.date:  # Nur Events mit gültigem Datum
                day = event.date.day
                grouped.setdefault(day, []).append(event)
        return grouped

    def formatday(self, day, weekday):
        """
        Gibt das HTML für eine einzelne Tageszelle zurück.
        :param day: Der Tag im Monat (1–31 oder 0 für leere Zelle)
        :param weekday: Wochentag (0=Mo, 6=So)
        :return: HTML-String für <td>
        """
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # Leere Zelle

        cssclass = self.cssclasses[weekday]         # Wochentag-Klasse z. B. "mon"
        events = self.events.get(day, [])           # Events für diesen Tag

        if events:
            cssclass += ' filled'                   # Zusätzliche CSS-Klasse für Tage mit Events
            event_list = "<ul>" + "".join(f"<li>{e.title}</li>" for e in events) + "</ul>"
            return f'<td class="{cssclass}"><strong>{day}</strong>{event_list}</td>'

        return f'<td class="{cssclass}">{day}</td>'  # Zelle ohne Event