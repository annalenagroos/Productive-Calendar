
# Productive Calendar

Eine webbasierte Kalender- und Aufgabenverwaltungs-App, die strukturierte Planung, smarte Erinnerungen und eine klare Aufgabenübersicht vereint.

---

## 1. Projektname & Team

**Projektname:** Productive Calendar  
**Team:**  
- Rejhan Nuradini  
- Mergim Jahija  
- Anna-Lena Groos  

### Aufgabenverteilung

| Name         | Rolle                  | Zuständigkeiten |
|--------------|------------------------|------------------|
| Anna-Lena    | Backend-Entwicklung    | Datenbankmodell, Routenlogik, Authentifizierung |
| Mergim       | Frontend & UI-Design   | CSS-Styling, Layout, HTML-Templates |
| Rejhan       | Fullstack-Entwicklung  | Integration Frontend + Backend, Debugging, Featureentwicklung |

---

## 2. Projektbeschreibung – Was, Wie, Warum

### Was ist das Ziel?
Der *Productive Calendar* hilft Benutzer:innen dabei, Aufgaben effektiv zu planen, Fristen einzuhalten und ihre tägliche Produktivität zu steigern. Er kombiniert Kalender-, Aufgaben- und Benutzerverwaltung in einer kompakten Weblösung.

### Wie funktioniert das?
Das Projekt basiert auf dem Flask-Webframework (Python) und speichert Daten lokal mit SQLite. Die Nutzeroberfläche wird mit HTML5, CSS3 und JavaScript gestaltet.

### Warum dieses Projekt?
In Zeiten von Informationsflut ist es schwer, fokussiert zu bleiben. Die App zielt darauf ab, den Alltag durch visuelle Klarheit und einfache Bedienung produktiver zu machen – vor allem für Studierende und Teams in kleinen Projekten.

---

## 3. Iterativer Projektplan

| Woche | Zeitraum         | Meilensteine |
|-------|------------------|--------------|
| 1     | 29.03 – 04.04    | Grundstruktur, Setup, Registrierung & Login |
| 2     | 05.04 – 11.04    | Aufgabenverwaltung & Dashboard |
| 3     | 12.04 – 18.04    | Kalender-Integration & UX-Verfeinerung |
| 4     | 19.04 – 23.04    | Tests, Dokumentation, Präsentation |

---

## 4. Minimalziel – Detailliert

**Ein funktionsfähiger Prototyp mit folgenden Kernfunktionen:**

- User Registration & Login (Sessions, Zugriffsschutz)
- Aufgaben anlegen, anzeigen und löschen
- Dashboard mit Übersicht aller Aufgaben
- Lokale Datenspeicherung (SQLite)
- Einfache Benutzeroberfläche mit Navigation
- Projekt lokal ausführbar per `flask run` oder `python app.py`

---

## 5. Erweiterte Ziele (Iterationsidee)

1. **Benachrichtigungen & Erinnerungen**
   - Anzeige von Aufgaben, die heute oder morgen fällig sind
   - Visuelle Hinweise im Dashboard

2. **Statistiken & Produktivitäts-Insights**
   - Diagramme zu offenen vs. erledigten Tasks (z. B. via Chart.js)
   - Motivierende Übersicht (z. B. „5 Aufgaben erledigt“)

3. **Wiederkehrende Aufgaben**
   - Automatisches Erstellen wiederholter Tasks
   - Optionen: täglich, wöchentlich, monatlich

4. **Responsive Design / Mobile View**
   - Optimierung für mobile Endgeräte

5. **Dark Mode (optional)**

---

## 6. Beispiel-User-Journey

1. Nutzer registriert sich mit E-Mail & Passwort
2. Login führt zum Dashboard mit leerer Aufgabenliste
3. Über ein Formular erstellt er eine neue Aufgabe
4. Aufgabe erscheint im Kalender am gewählten Datum
5. Eine Benachrichtigung zeigt an, wenn eine Aufgabe heute fällig ist
6. Der Nutzer kann Aufgaben als erledigt markieren oder löschen

---

## 7. Features (detailliert)

| Feature                         | Beschreibung |
|----------------------------------|--------------|
| **Login & Registrierung**     | Authentifizierung mit Passwort-Validierung und Login-Schutz |
| **Aufgabenverwaltung**        | Erstellen, Anzeigen, Löschen und Zuweisung von Aufgaben |
| **Kalenderansicht**          | Aufgaben erscheinen nach Datum visuell im Kalender |
| **Reminder-Funktion**         | Visuelle Warnung bei nahenden Deadlines |
| **Profilverwaltung**         | Nutzer können Profil bearbeiten oder löschen |
| **Lokale Speicherung**       | Alle Daten werden mit SQLite gespeichert |

---

## 8. Installation & Ausführen

### Voraussetzungen

- Python 3.10 oder neuer
- Virtuelle Umgebung (empfohlen)

### Starten der App

```bash
# Methode A (empfohlen):
export FLASK_APP=app.py     # oder: set FLASK_APP=app.py (Windows)
flask run

# Methode B (direkt):
python app.py
```

➡ Die App ist dann unter **http://127.0.0.1:5000/** erreichbar

---

## 9. Verwendete Technologien & Tools

| Kategorie      | Technologie         |
|----------------|---------------------|
| **Backend**    | Flask (Python), SQLite |
| **Frontend**   | HTML5, CSS3, JavaScript |
| **Entwicklung**| Visual Studio Code, Git |
| **Teamarbeit** | Discord, GitHub |

---

## 10. Verzeichnisstruktur

```
Productive-Calendar/
├── app.py                  # Hauptdatei für die Flask-App
├── models.py               # Datenbank-Modelle
├── requirements.txt        # Abhängigkeiten
├── README.md               # Projektdokumentation
│
├── instance/
│   └── database.db         # SQLite-Datenbank
│
├── static/
│   ├── style.css           # Design (CSS)
│   └── script.js           # Interaktive Funktionen
│
├── templates/
│   ├── layout.html         # Basislayout
│   ├── index.html          # Startseite
│   ├── dashboard.html      # Hauptübersicht
│   ├── login.html          # Loginmaske
│   ├── register.html       # Registrierung
│   ├── delete_profile.html # Profil löschen
│   ├── edit_profile.html   # Profil bearbeiten
│   └── profile.html        # Benutzerprofil
```

---

## Abgabe

**Projektzeitraum:** 29.03.2025 – 26.04.2025  
**Finale Abgabe:** **26.04.2025**
