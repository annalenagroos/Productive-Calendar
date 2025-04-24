import argparse
from database import add_event

def main():
    parser = argparse.ArgumentParser(description="Event hinzufügen")
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--category", default="Allgemein")
    args = parser.parse_args()

    add_event(title=args.title, date=args.date, category=args.category)
    print(f"Event hinzugefügt: {args.title} am {args.date}")

if __name__ == "__main__":
    main()
