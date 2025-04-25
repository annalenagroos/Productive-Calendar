# ===================== IMPORTS =====================
from extensions import db
from datetime import datetime

# ===================== BENUTZERMODELL =====================
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Beziehungen
    events = db.relationship('Event', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)


# ===================== EVENTMODELL =====================
class Event(db.Model):
    __tablename__ = "event"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    repeat = db.Column(db.String(20), default='none')
    is_archived = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# ===================== TASKMODELL =====================
class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)