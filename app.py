from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from markupsafe import Markup
from io import StringIO, BytesIO
import csv
import io
import calendar

# Eigene Module
from extensions import db
from models import User, Task, Event
from custom_calendar import EventCalendar
from calendar_tools import export_all_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.secret_key = "dein_sicherer_key"
db.init_app(app)

# ------------------- Auth -------------------
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
        flash('Login fehlgeschlagen.')
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
        if request.form['username']:
            user.username = request.form['username']
        if request.form['password']:
            user.password = request.form['password']
        db.session.commit()
        flash('Profil aktualisiert.')
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

# ------------------- Dashboard & Events -------------------
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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    if request.method == 'POST':
        if 'event_title' in request.form:
            new_event = Event(
                title=request.form['event_title'],
                date=datetime.strptime(request.form['event_date'], '%Y-%m-%d'),
                repeat=request.form.get('event_repeat', 'none'),
                user_id=user_id
            )
            db.session.add(new_event)
            db.session.commit()
        elif 'task_description' in request.form:
            new_task = Task(description=request.form['task_description'], user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('dashboard'))

    events_raw = Event.query.filter_by(user_id=user_id).all()
    events = expand_recurring(events_raw)
    tasks = Task.query.filter_by(user_id=user_id).all()
    archived_tasks = Task.query.filter_by(user_id=user_id, is_archived=True).all()
    archived_events = Event.query.filter_by(user_id=user_id, is_archived=True).all()
    cal = EventCalendar(events)
    month_calendar = Markup(cal.formatmonth(datetime.now().year, datetime.now().month))
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.done])
    completion_rate = round((completed_tasks / total_tasks) * 100) if total_tasks else 0

    return render_template('dashboard.html', events=events, tasks=tasks,
        archived_tasks=archived_tasks, archived_events=archived_events,
        now=datetime.now(), month_calendar=month_calendar,
        total_tasks=total_tasks, completed_tasks=completed_tasks,
        completion_rate=completion_rate)

@app.route('/event/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    event = Event.query.filter_by(id=id, user_id=session['user_id']).first_or_404()
    if request.method == 'POST':
        event.title = request.form['title']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        db.session.commit()
        flash("Termin aktualisiert!")
        return redirect(url_for('dashboard'))
    return render_template('edit_event.html', event=event)

# ------------------- Task- und Eventfunktionen -------------------
@app.route('/task/done/<int:id>')
def task_done(id):
    task = Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/task/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/event/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('dashboard'))

# ------------------- Kalender & API -------------------
@app.route('/calendar')
def calendar_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('calendar.html')

@app.route('/api/events')
def get_events():
    all_events = Event.query.all()
    return jsonify([
        {'title': e.title, 'start': e.date.strftime('%Y-%m-%d'), 'color': '#3a87ad'}
        for e in all_events
    ])

# ------------------- CSV-Export & Backup -------------------
@app.route('/export')
def export():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    output = StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["Typ", "Titel/Beschreibung", "Datum/Status"])
    for event in Event.query.filter_by(user_id=session['user_id']):
        writer.writerow(["Termin", event.title, event.date])
    for task in Task.query.filter_by(user_id=session['user_id']):
        writer.writerow(["Aufgabe", task.description, "Erledigt" if task.done else "Offen"])
    output.seek(0)
    return send_file(BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='kalender_export.csv')

@app.route('/backup')
def backup():
    return export()  # nutzt dieselbe Logik wie oben

# ------------------- Suche & Filter -------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    search_term = request.form.get('search_term')
    event_date = request.form.get('event_date')
    filter_type = request.form.get('filter_type')
    events, tasks = [], []

    if request.method == 'POST':
        if filter_type in [None, '', 'event']:
            query = Event.query.filter_by(user_id=user_id)
            if search_term:
                query = query.filter(Event.title.ilike(f'%{search_term}%'))
            if event_date:
                query = query.filter(Event.date == event_date)
            events = query.all()
        if filter_type in [None, '', 'task']:
            query = Task.query.filter_by(user_id=user_id)
            if search_term:
                query = query.filter(Task.description.ilike(f'%{search_term}%'))
            tasks = query.all()

    return render_template('search.html', events=events, tasks=tasks,
                           search_term=search_term, event_date=event_date, filter_type=filter_type)

@app.route('/export-filter', methods=['GET', 'POST'])
def export_filtered():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('export.html')

    user_id = session['user_id']
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    filter_type = request.form.get('filter_type')

    events, tasks = [], []
    if filter_type in ['all', 'event']:
        query = Event.query.filter_by(user_id=user_id)
        if from_date:
            query = query.filter(Event.date >= from_date)
        if to_date:
            query = query.filter(Event.date <= to_date)
        events = query.all()
    if filter_type in ['all', 'task']:
        tasks = Task.query.filter_by(user_id=user_id).all()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow(['Typ', 'Titel/Beschreibung', 'Datum/Status'])
    for event in events:
        writer.writerow(['Termin', event.title, event.date])
    for task in tasks:
        writer.writerow(['Aufgabe', task.description, 'Erledigt' if task.done else 'Offen'])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='gefilterter_export.csv')

# ------------------- Fehlerbehandlung -------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ------------------- Start -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)