import argparse
import csv
from database import add_event
from app import Event, db, app
import analytics


def add_event_command(args):
    add_event(
        title=args.title,
        date=args.date,
        category=args.category,
        description=args.description
    )
    print(f"✅ Event hinzugefügt: {args.title} am {args.date}")


def list_events_command(args):
    events = Event.query.all()
    for e in events:
        print(f"[{e.id}] {e.title} | {e.date} | {e.category} | {e.description}")


def delete_event_command(args):
    event = db.session.get(Event, args.id)
    if not event:
        print(f"❌ Kein Event mit ID {args.id} gefunden.")
        return
    db.session.delete(event)
    db.session.commit()
    print(f"🗑️ Event mit ID {args.id} gelöscht.")


def edit_description_command(args):
    event = db.session.get(Event, args.id)
    if not event:
        print(f"❌ Kein Event mit ID {args.id} gefunden.")
        return
    old_desc = event.description
    event.description = args.description
    db.session.commit()
    print(f"✏️ Beschreibung aktualisiert: '{old_desc}' → '{args.description}'")


def search_events_command(args):
    query = args.query.lower() if args.query else None
    category = args.category.lower() if args.category else None
    date = args.date if args.date else None

    results = Event.query.all()
    filtered = []

    for e in results:
        match_query = query in e.title.lower() or query in e.description.lower() if query else True
        match_category = category == e.category.lower() if category else True
        match_date = str(e.date.date()) == date if date else True

        if match_query and match_category and match_date:
            filtered.append(e)

    if not filtered:
        print("🔍 Keine passenden Events gefunden.")
    else:
        print("🔍 Gefundene Events:")
        for e in filtered:
            print(f"[{e.id}] {e.title} | {e.date} | {e.category} | {e.description}")

        if args.export:
            with open(args.export, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Titel", "Datum", "Kategorie", "Beschreibung"])
                for e in filtered:
                    writer.writerow([e.id, e.title, e.date, e.category, e.description])
            print(f"💾 Ergebnisse exportiert nach: {args.export}")


def stats_command(args):
    print("\n📊 Event-Statistiken:")
    print("- Events nach Monat:", analytics.get_event_counts_by_month())
    print("- Events nach Wochentag:", analytics.get_event_counts_by_weekday())
    print("- Aufgabenstatus:", analytics.get_task_completion_stats())
    print("- Tageszeiten-Verteilung:", analytics.get_event_distribution_by_time())
    print("- Durchschnitt Events pro Tag:", analytics.get_average_events_per_day())
    print("- Vergangenheit vs. Zukunft:", analytics.get_event_time_stats())
    print("- Top Tage:", analytics.get_top_event_days())


def main():
    parser = argparse.ArgumentParser(description="Productive Calendar CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    parser_add = subparsers.add_parser("add", help="Event hinzufügen")
    parser_add.add_argument("--title", required=True)
    parser_add.add_argument("--date", required=True)
    parser_add.add_argument("--category", default="Allgemein")
    parser_add.add_argument("--description", required=True)
    parser_add.set_defaults(func=add_event_command)

    # list
    parser_list = subparsers.add_parser("list", help="Alle Events anzeigen")
    parser_list.set_defaults(func=list_events_command)

    # delete
    parser_delete = subparsers.add_parser("delete", help="Event löschen")
    parser_delete.add_argument("--id", type=int, required=True)
    parser_delete.set_defaults(func=delete_event_command)

    # edit-description
    parser_edit = subparsers.add_parser("edit-description", help="Beschreibung eines Events bearbeiten")
    parser_edit.add_argument("--id", type=int, required=True)
    parser_edit.add_argument("--description", required=True)
    parser_edit.set_defaults(func=edit_description_command)

    # search
    parser_search = subparsers.add_parser("search", help="Events nach Stichwort, Kategorie oder Datum suchen")
    parser_search.add_argument("--query", required=False)
    parser_search.add_argument("--category", required=False)
    parser_search.add_argument("--date", required=False, help="Format: YYYY-MM-DD")
    parser_search.add_argument("--export", required=False, help="Pfad zur Export-CSV-Datei")
    parser_search.set_defaults(func=search_events_command)

    # stats
    parser_stats = subparsers.add_parser("stats", help="Statistiken anzeigen")
    parser_stats.set_defaults(func=stats_command)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        with app.app_context():
            args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()