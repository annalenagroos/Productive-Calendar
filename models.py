from flask_sqlalchemy import SQLAlchemy

# Initialisierung der SQLAlchemy-Datenbankinstanz
db = SQLAlchemy()

# Modell für Benutzer (User)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel für den Benutzer
    username = db.Column(db.String(150), unique=True, nullable=False)  # Benutzername, muss einzigartig und nicht null sein
    password = db.Column(db.String(150), nullable=False)  # Passwort, darf nicht null sein
    # Beziehung zu Ereignissen (Events) und Aufgaben (Tasks)
    # Diese Beziehungen stellen sicher, dass die zugehörigen Aufgaben und Ereignisse gelöscht werden,
    # wenn der Benutzer gelöscht wird (ondelete="CASCADE").
    events = db.relationship('Event', backref='user', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')

# Modell für Ereignisse (Event)
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel für das Ereignis
    title = db.Column(db.String(150), nullable=False)  # Titel des Ereignisses, darf nicht null sein
    date = db.Column(db.Date, nullable=False)  # Datum des Ereignisses, darf nicht null sein
    # ForeignKey für die Beziehung zum Benutzer, der das Ereignis erstellt hat
    # 'user.id' verweist auf den Primärschlüssel der User-Tabelle
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

# Modell für Aufgaben (Task)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel für die Aufgabe
    description = db.Column(db.String(250), nullable=False)  # Beschreibung der Aufgabe, darf nicht null sein
    done = db.Column(db.Boolean, default=False)  # Status der Aufgabe (ob erledigt oder nicht), Standardwert ist 'False' (nicht erledigt)
    # ForeignKey für die Beziehung zum Benutzer, der die Aufgabe erstellt hat
    # 'user.id' verweist auf den Primärschlüssel der User-Tabelle
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))