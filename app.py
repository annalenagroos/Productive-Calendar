from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import io
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# ------------------- Datenbankmodelle -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    repeat = db.Column(db.String(20), default='none')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    repeat = db.Column(db.String(20), default='none')

# ------------------- Auth & Benutzer -------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Benutzername existiert bereits!')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrierung erfolgreich!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        flash('Login fehlgeschlagen. Überprüfe Benutzername und Passwort.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        current_password = request.form['current-password']
        new_username = request.form['username']
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']

        # Aktuelles Passwort prüfen
        if not check_password_hash(user.password, current_password):
            flash('Das aktuelle Passwort ist falsch.')
            return redirect(url_for('edit_profile'))

        # Benutzernamen aktualisieren
        if new_username:
            user.username = new_username

        # Neues Passwort prüfen und aktualisieren
        if new_password:
            if new_password != confirm_password:
                flash('Die neuen Passwörter stimmen nicht überein.')
                return redirect(url_for('edit_profile'))
            user.password = generate_password_hash(new_password)

        db.session.commit()
        flash('Profil erfolgreich aktualisiert.')
        return redirect(url_for('dashboard'))

    return render_template('edit_profile.html', user=user)

@app.route('/profile/delete', methods=['GET', 'POST'])
def delete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        Task.query.filter_by(user_id=user.id).delete()
        Event.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)
        flash('Dein Profil wurde gelöscht.')
        return redirect(url_for('index'))

    return render_template('delete_profile.html', user=user)

# ------------------- Wiederholende Termine aufbereiten -------------------
def expand_recurring(events):
    expanded = []
    today = datetime.today().date()
    for event in events:
        expanded.append(event)
        for i in range(1, 5):
            new_date = None
            if event.repeat == 'daily':
                new_date = event.date + timedelta(days=i)
            elif event.repeat == 'weekly':
                new_date = event.date + timedelta(weeks=i)
            elif event.repeat == 'monthly':
                try:
                    month = event.date.month + i
                    year = event.date.year + (month - 1) // 12
                    month = (month - 1) % 12 + 1
                    new_date = event.date.replace(year=year, month=month)
                except ValueError:
                    continue
            if new_date and new_date >= today:
                expanded.append(Event(title=event.title + " (Wdh)", date=new_date, user_id=event.user_id))
    return expanded

def expand_tasks(tasks):
    expanded = []
    today = datetime.today().date()
    for task in tasks:
        expanded.append(task)
        for i in range(1, 5):
            if task.repeat == 'daily':
                due_date = today + timedelta(days=i)
            elif task.repeat == 'weekly':
                due_date = today + timedelta(weeks=i)
            else:
                continue

            clone = Task(
                description=f"{task.description} (Wdh)",
                done=False,
                user_id=task.user_id,
                repeat='none'  # geklonte Tasks sind einmalig sichtbar
            )
            expanded.append(clone)
    return expanded

# ------------------- Dashboard -------------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        if 'event_title' in request.form:
            title = request.form['event_title']
            date = datetime.strptime(request.form['event_date'], '%Y-%m-%d')
            repeat = request.form.get('event_repeat', 'none')
            new_event = Event(title=title, date=date, user_id=user_id, repeat=repeat)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('dashboard'))

        if 'task_description' in request.form:
            description = request.form['task_description']
            repeat = request.form.get('task_repeat', 'none')
            new_task = Task(description=description, user_id=user_id, repeat=repeat)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('dashboard'))

    year = datetime.now().year
    month = datetime.now().month
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    month_calendar = cal.formatmonth(year, month)

    events_raw = Event.query.filter_by(user_id=user_id).all()
    events = expand_recurring(events_raw)
    tasks_raw = Task.query.filter_by(user_id=user_id).all()
    tasks = expand_tasks(tasks_raw)

    return render_template('dashboard.html', events=events, tasks=tasks, now=datetime.now(), month_calendar=month_calendar)

# ------------------- Aufgabenaktionen -------------------
@app.route('/task/done/<int:id>')
def task_done(id):
    task = Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()

    # Falls erledigt und Wiederholung aktiv: neue Aufgabe erstellen
    if task.done and task.repeat != 'none':
        next_date = None
        if task.repeat == 'daily':
            next_date = datetime.today() + timedelta(days=1)
        elif task.repeat == 'weekly':
            next_date = datetime.today() + timedelta(weeks=1)

    if next_date:
        existing = Task.query.filter_by(
        description=task.description,
        user_id=task.user_id,
        done=False
         ).first()
    
    if not existing:
        new_task = Task(
            description=task.description,
            done=False,
            user_id=task.user_id,
            repeat=task.repeat
        )
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/task/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

# ------------------- Ereignisse -------------------
@app.route('/event/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/event/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    event = Event.query.get_or_404(id)

    if request.method == 'POST':
        event.title = request.form['event_title']
        event.date = datetime.strptime(request.form['event_date'], '%Y-%m-%d')
        event.repeat = request.form.get('event_repeat', 'none')
        db.session.commit()
        flash('Termin wurde aktualisiert.')
        return redirect(url_for('dashboard'))

    return render_template('edit_event.html', event=event)

# ------------------- Export CSV -------------------
@app.route('/export')
def export():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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

# ------------------- API für Kalender -------------------
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

# ------------------- Suche -------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    search_term = request.form.get('search_term')
    event_date = request.form.get('event_date')
    filter_type = request.form.get('filter_type')

    events = []
    tasks = []

    if request.method == 'POST':
        if filter_type in [None, '', 'event']:
            events_query = Event.query.filter(Event.user_id == user_id)
            if search_term:
                events_query = events_query.filter(Event.title.ilike(f'%{search_term}%'))
            if event_date:
                events_query = events_query.filter(Event.date == event_date)
            events = events_query.all()

        if filter_type in [None, '', 'task']:
            tasks_query = Task.query.filter(Task.user_id == user_id)
            if search_term:
                tasks_query = tasks_query.filter(Task.description.ilike(f'%{search_term}%'))
            tasks = tasks_query.all()

    return render_template('search.html', events=events, tasks=tasks,
                           search_term=search_term, event_date=event_date, filter_type=filter_type)

# ------------------- App starten -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)