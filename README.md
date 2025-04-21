# Productive Calendar

Productive Calendar ist eine webbasierte Kalender- und Aufgabenverwaltungs-App, die dir hilft, deinen Alltag produktiver zu gestalten. Sie kombiniert Kalenderfunktionen mit einer einfachen Benutzer- und Aufgabenverwaltung in einem übersichtlichen Interface.

Team: Rejhan Nuradini, Mergim Jahija, Anna-Lena Groos

Aufgabenverteilung:

- **Anna-Lena:** Entwicklung
- **Mergim:** Design
- **Rejhan:** Design & Entwicklung

# Projekt-Zeitplan: 29.03.2025 – 23.04.2025

Ein realistischer Zeitplan für das Projekt **„Productive Calendar“**, aufgeteilt nach Wochen mit passenden Aufgabenpaketen.

## Woche 1 – Projektaufbau & Grundfunktionen (29.03. – 04.04.)

- Projektstruktur einrichten (Flask, Ordner, Git)
- Setup der Entwicklungsumgebung (Python, virtualenv, requirements.txt)
- Startseite & erste Routen (z. B. `/`, `/login`)
- Datenbankmodell: User und Task erstellen
- Login- & Registrierungsfunktion (HTML + Backend)

## Woche 2 – Aufgabenverwaltung & Dashboard (05.04. – 11.04.)

- Aufgabenformular: neue Aufgaben anlegen
- Aufgaben im Dashboard anzeigen & löschen
- Start der Kalenderintegration (Basislayout)
- Erste Design-Verbesserungen (CSS-Styling, Layout)

## Woche 3 – Kalender & Zusatzfunktionen (12.04. – 18.04.)

- Kalender vollständig integrieren
- Aufgaben in Kalender anzeigen (Datum zuweisen)

## Woche 4 – Feinschliff & Dokumentation (19.04. – 23.04.)

- README vervollständigen (mit Anleitung)
- Projekt testen: Bugs beheben, kleine Verbesserungen
- Präsentationsvorbereitung: Projekt vorstellen können
- Finale Abgabe vorbereiten

### Abgabebereit am: **25.04.2025**


## Verwendete Technologien und Tools

- Discord für die Kommunikation
- Visual Studio Code (Entwicklungsumgebung)
- Python, CSS und HTML als Programmiersprachen
- **Backend:** Flask, SQLite
- **Frontend:** HTML5, CSS3

## Minimale Ziele

1. **Projektgrundstruktur erstellen**

Ziel: Eine funktionierende Flask-Applikation mit grundlegender Struktur.

- Flask-App app.py aufsetzen
- templates/, static/ und instance/-Ordner anlegen
- erste Route (/) mit einer simplen HTML-Seite anzeigen
- requirements.txt erstellen
- Projekt lokal startbar machen (flask run)

2. **Benutzerregistrierung & Login implementieren**

Ziel: Nutzer können sich registrieren, einloggen und das Profil löschen.
- HTML-Formulare: register.html und login.html
- Flask-Login oder manuelles Session-Handling
- Validierung von Eingaben
- SQLite-Tabelle users erstellen
- Schutz von Routen (z. B. /Dashboard nur mit Login erreichbar)

3. **Aufgabenverwaltung aufbauen**

Ziel: Nutzer können Aufgaben anlegen, ansehen und löschen.
- models.py: Tabelle tasks mit Feldern wie Titel, Beschreibung, Datum, User-ID
- HTML-Formular zur Erstellung neuer Aufgaben
- Liste der Aufgaben im dashboard.html anzeigen
- Aufgaben löschen können

## Features

- Benutzerregistrierung & Login-System
- Aufgaben anlegen, anzeigen und verwalten
- Kalenderansicht zur besseren Planung
- Dashboard mit Übersicht der Aufgaben
- Speicherung der Daten
- Frontend mit HTML/CSS/JavaScript
- Backend mit Flask (Python)

## Erweiterte Ziele

1. **Benachrichtigungssystem / Erinnerung**

Ziel: Nutzer erhalten visuelle Erinnerungen an anstehende Aufgaben.
- Anzeige von Aufgaben, die „heute“ oder „morgen“ fällig sind (z. B. in roter Box oben)
- Optional: E-Mail-Erinnerung (via Flask-Mail)
- Visualisierung: kleine Glocke im Dashboard mit „x neue Aufgaben für heute“
- Aufgaben farblich markieren, wenn sie bald fällig oder überfällig sind

2. **Statistik-Dashboard für persönliche Produktivität**

Ziel: Übersicht, wie produktiv der Nutzer war.
- Balken- oder Kreisdiagramm: erledigte vs. offene Aufgaben
- Anzeige: „Du hast diese Woche 5 Aufgaben erledigt“
- Nutzung von Chart.js oder Plotly (Frontend-Charting-Bibliothek)
- Integration ins Dashboard

3. **Wiederkehrende Aufgaben**

Ziel: Aufgaben, die regelmässig auftauchen (z. B. jede Woche, jeden Monat).
- Beim Erstellen: Option „Wöchentlich“, „Täglich“, etc.
- Beim Speichern: neue Aufgabe wird automatisch geklont mit neuem Datum
- Herausforderung: Logik & Datenbankdesign etwas komplexer

## Installation

## 1. App starten – Zwei Wege

### Standardmethode (empfohlen): `flask run`

#### Für Windows:
```bash
set FLASK_APP=app.py
flask run
```

#### Für macOS / Linux:
```bash
export FLASK_APP=app.py
flask run
```

---

### Alternative (einfach & direkt): `python app.py`

```bash
python app.py
```

-> Ideal für Einsteiger. Diese Methode startet die App direkt, ohne Umgebungsvariable.

---

### Projekt im Browser öffnen
Die App läuft nun lokal unter:

**http://127.0.0.1:5000/**



## Verzeichnisstruktur

```
Productive-Calendar/
│
├── app.py                  # Flask-Anwendung
├── models.py               # Datenbankmodelle, Routen und Views
├── requirements.txt        # Abhängigkeiten
├── README.md               # Projektdokumentation
│
├── instance/
│   ├── database.db         # SQLite-Datenbank
│   └── dashboard.db        # Weitere Datenbankdatei
│
├── static/
│   ├── style.css           # CSS-Design
│   └── script.js           # JavaScript-Funktionalität
│
├── templates/
│   ├── layout.html         # Gemeinsames Layout
│   ├── index.html          # Startseite
│   ├── dashboard.html      # Aufgabenübersicht
│   ├── login.html          # Login-Formular
│   ├── register.html       # Registrierungsformular
│   ├── delete_profile.html # Profil löschen
│   ├── edit_profile.html   # Profil bearbeiten
│   ├── profile.html        # Benutzerprofil
│   └── register.html       # Registrierungsformular
```