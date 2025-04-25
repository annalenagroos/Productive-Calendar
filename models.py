# ===================== IMPORTS =====================
from extensions import db                      # SQLAlchemy-Datenbankinstanz
from datetime import datetime                  # Für Zeit- und Datumswerte

# ===================== BENUTZERMODELL =====================
class User(db.Model):
    """
    Repräsentiert einen Benutzer mit Login-Daten und Beziehungen zu Events & Tasks.
    """
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}  # Ermöglicht das Neuladen bei Reloads/Tests

    id = db.Column(db.Integer, primary_key=True)                        # Eindeutige ID
    username = db.Column(db.String(150), unique=True, nullable=False)  # Benutzername (muss einzigartig sein)
    password = db.Column(db.String(150), nullable=False)               # Passwort (gehasht)

    # Beziehungen zu Events und Tasks
    events = db.relationship('Event', backref='user', lazy=True)       # Alle Events dieses Users
    tasks = db.relationship('Task', backref='user', lazy=True)         # Alle Tasks dieses Users

# ===================== EVENTMODELL =====================
class Event(db.Model):
    """
    Repräsentiert einen Termin mit Titel, Datum, Wiederholungsregel, Archivstatus.
    Verknüpft mit einem Benutzer über user_id.
    """
    __tablename__ = "event"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)           # Titel des Events
    date = db.Column(db.Date, nullable=False)                   # Datum des Events
    repeat = db.Column(db.String(20), default='none')           # Wiederholung (z. B. daily, weekly)
    is_archived = db.Column(db.Boolean, default=False)          # Ob archiviert

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Verknüpfung zum User

# ===================== TASKMODELL =====================
class Task(db.Model):
    """
    Repräsentiert eine To-Do-Aufgabe mit Beschreibung, Erledigt-Status und Archivierung.
    Verknüpft mit einem Benutzer.
    """
    __tablename__ = "task"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)     # Beschreibung der Aufgabe
    done = db.Column(db.Boolean, default=False)                 # Ob erledigt
    is_archived = db.Column(db.Boolean, default=False)          # Ob archiviert

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Verknüpfung zum User