# Productive Calendar

Productive Calendar ist eine webbasierte Kalender- und Aufgabenverwaltungs-App, die dir hilft, deinen Alltag produktiver zu gestalten. Sie kombiniert Kalenderfunktionen mit einer einfachen Benutzer- und Aufgabenverwaltung in einem übersichtlichen Interface.

## Features

- Benutzerregistrierung & Login-System
- Aufgaben anlegen, anzeigen und verwalten
- Kalenderansicht zur besseren Planung
- Dashboard mit Übersicht der Aufgaben
- Speicherung der Daten
- Frontend mit HTML/CSS/JavaScript
- Backend mit Flask (Python)

## Installation

1. **Abhängigkeiten installieren**

```bash
pip install -r requirements.txt
```

2. **App starten**

```bash
export FLASK_APP=app.py     # für Unix/macOS
set FLASK_APP=app.py        # für Windows

flask run
```

3. **Im Browser öffnen**

Standardmäßig unter: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Verzeichnisstruktur

```
Productive-Calendar/
│
├── app.py                  # Flask-Anwendung
├── models.py               # Datenbankmodelle
├── routes.py               # Routen und Views
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
│   └── register.html       # Registrierungsformular
```

## Verwendete Technologien

- **Backend:** Flask, SQLite
- **Frontend:** HTML5, CSS3