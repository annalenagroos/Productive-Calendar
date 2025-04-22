from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import io
import calendar

# Flask-Anwendung initialisieren
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'  # Verbindung zur SQLite-Datenbank
app.config['SECRET_KEY'] = 'supersecretkey'  # Session-Schlüssel für sichere Cookies und Sessions
db = SQLAlchemy(app)

# Modell für Benutzer
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Modell für Ereignisse
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Modell für Aufgaben
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Startseite - Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Registrierungsroute
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Überprüfe, ob der Benutzername bereits existiert
        if User.query.filter_by(username=username).first():
            flash('Benutzername existiert bereits!')
            return redirect(url_for('register'))
        
        # Passwort hashen, bevor es in der DB gespeichert wird
        password_hash = generate_password_hash(password)
        
        # Neuen Benutzer anlegen
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()  # Speichert den neuen Benutzer in der DB
        flash('Registrierung erfolgreich!')
        return redirect(url_for('login'))  # Weiterleitung zum Login
    
    return render_template('register.html')

# Loginroute
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Benutzer aus der DB holen
        user = User.query.filter_by(username=username).first()
        
        # Passwort überprüfen
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Benutzer-ID in der Session speichern
            return redirect(url_for('dashboard'))  # Weiterleitung zum Dashboard
        
        flash('Login fehlgeschlagen. Überprüfe Benutzername und Passwort.')
    
    return render_template('login.html')

# Logout-Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Benutzersession löschen
    return redirect(url_for('index'))  # Zur Startseite weiterleiten

# Profilbearbeitungsroute
@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Sicherstellen, dass der Benutzer eingeloggt ist

    user = User.query.get_or_404(session['user_id'])  # Benutzer aus der Datenbank holen

    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        
        # Wenn ein neuer Benutzername eingegeben wurde, diesen aktualisieren
        if new_username:
            user.username = new_username
        
        # Wenn ein neues Passwort eingegeben wurde, dieses aktualisieren
        if new_password:
            user.password = new_password
        
        db.session.commit()  # Änderungen speichern
        flash('Profil erfolgreich aktualisiert.')  # Erfolgsmeldung anzeigen
        return redirect(url_for('dashboard'))  # Zurück zum Dashboard weiterleiten

    return render_template('edit_profile.html', user=user)

# Profil löschen
@app.route('/profile/delete', methods=['GET', 'POST'])
def delete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Sicherstellen, dass der Benutzer eingeloggt ist

    user = User.query.get_or_404(session['user_id'])  # Benutzerobjekt laden

    if request.method == 'POST':
        Task.query.filter_by(user_id=user.id).delete()  # Alle Aufgaben des Benutzers löschen
        Event.query.filter_by(user_id=user.id).delete()  # Alle Ereignisse des Benutzers löschen
        db.session.delete(user)  # Benutzer löschen
        db.session.commit()  # Änderungen speichern
        session.pop('user_id', None)  # Session des Benutzers löschen
        flash('Dein Profil wurde gelöscht.')  # Erfolgsmeldung anzeigen
        return redirect(url_for('index'))  # Zur Startseite weiterleiten

    return render_template('delete_profile.html', user=user)

# Dashboard-Routen für Aufgaben und Ereignisse
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Sicherstellen, dass der Benutzer eingeloggt ist

    user_id = session['user_id']

    if request.method == 'POST':
        if 'event_title' in request.form:
            title = request.form['event_title']
            date = datetime.strptime(request.form['event_date'], '%Y-%m-%d')
            new_event = Event(title=title, date=date, user_id=user_id)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if 'task_description' in request.form:
            description = request.form['task_description']
            new_task = Task(description=description, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('dashboard'))

    # Kalender für den aktuellen Monat erstellen
    year = datetime.now().year
    month = datetime.now().month
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    month_calendar = cal.formatmonth(year, month)

    # Events und Tasks aus der Datenbank abfragen
    events = Event.query.filter_by(user_id=user_id).all()
    tasks = Task.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', events=events, tasks=tasks, now=datetime.now(), month_calendar=month_calendar)

# Aufgabe als erledigt markieren
@app.route('/task/done/<int:id>')
def task_done(id):
    task = Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('dashboard'))

# Aufgabe löschen
@app.route('/task/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

# Ereignis löschen
@app.route('/event/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('dashboard'))

# Export von Ereignissen und Aufgaben als CSV
@app.route('/export')
def export():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Sicherstellen, dass der Benutzer eingeloggt ist

    user_id = session['user_id']
    events = Event.query.filter_by(user_id=user_id).all()
    tasks = Task.query.filter_by(user_id=user_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Typ', 'Titel/Beschreibung', 'Datum/Status'])

    for event in events:
        writer.writerow(['Termin', event.title, event.date])

    for task in tasks:
        writer.writerow(['Aufgabe', task.description, 'Erledigt' if task.done else 'Offen'])

    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='kalender_export.csv')

# API für Ereignisse
@app.route('/api/events')
def api_events():
    if 'user_id' not in session:
        return jsonify([])

    user_id = session['user_id']
    events = Event.query.filter_by(user_id=user_id).all()

    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.date.isoformat()
        })

    return jsonify(event_list)

# Suchfunktion für Ereignisse und Aufgaben
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Sicherstellen, dass der Benutzer eingeloggt ist

    user_id = session['user_id']
    search_term = None
    events = []
    tasks = []

    if request.method == 'POST':
        search_term = request.form['search_term']  # Den Suchbegriff aus dem Formular erhalten
        
        # Ereignisse suchen
        events = Event.query.filter(
            Event.title.ilike(f'%{search_term}%'),  # 'ilike' für fallunabhängige Suche
            Event.user_id == user_id  # Nur Ereignisse des eingeloggten Benutzers
        ).all()

        # Aufgaben suchen
        tasks = Task.query.filter(
            Task.description.ilike(f'%{search_term}%'),  # 'ilike' für fallunabhängige Suche
            Task.user_id == user_id  # Nur Aufgaben des eingeloggten Benutzers
        ).all()

    return render_template('search.html', events=events, tasks=tasks, search_term=search_term)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Diese Zeile sorgt dafür, dass alle Tabellen erstellt werden
    app.run(debug=True)
