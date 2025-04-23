# ===================== IMPORTS =====================
from app import db  # Importiert die SQLAlchemy-Instanz aus deiner Flask-App
from datetime import datetime  # Wird oft für Datumswerte gebraucht (z. B. für Events)

# ===================== BENUTZERMODELL =====================
class User(db.Model):
    """
    Datenbankmodell für einen Benutzer.
    Jeder Benutzer kann mehrere Events und Tasks besitzen.
    """
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID (automatisch generiert)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Benutzername, eindeutig & Pflichtfeld
    password = db.Column(db.String(150), nullable=False)  # Passwort (meist gehashed)

    # Optional: Beziehung zu Events und Tasks (nur bei Bedarf aktivieren)
    # events = db.relationship('Event', backref='user', lazy=True)
    # tasks = db.relationship('Task', backref='user', lazy=True)


# ===================== EVENTMODELL =====================
class Event(db.Model):
    """
    Datenbankmodell für ein Ereignis (Kalendereintrag).
    Verknüpft mit einem Benutzer (user_id als ForeignKey).
    """
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID
    title = db.Column(db.String(150), nullable=False)  # Titel des Events (Pflichtfeld)
    date = db.Column(db.Date, nullable=False)  # Datum des Events (Pflichtfeld, kein Uhrzeitteil)
    
    # Fremdschlüssel: Verknüpft dieses Event mit einem Benutzer
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Optionale Wiederholung: "none", "daily", "weekly", "monthly"
    repeat = db.Column(db.String(20), default='none')


# ===================== TASKMODELL =====================
class Task(db.Model):
    """
    Datenbankmodell für eine Aufgabe (To-do-Eintrag).
    Verknüpft mit einem Benutzer (user_id als ForeignKey).
    """
    id = db.Column(db.Integer, primary_key=True)  # Eindeutige ID
    description = db.Column(db.String(250), nullable=False)  # Beschreibung der Aufgabe (Pflichtfeld)

    done = db.Column(db.Boolean, default=False)  # Ob die Aufgabe erledigt wurde (Standard: Nein)

    # Fremdschlüssel: Verknüpfung zu einem Benutzer
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))