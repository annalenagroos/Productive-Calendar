from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Benutzername existiert bereits.')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
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
        new_username = request.form['username']
        new_password = request.form['password']
        if new_username:
            user.username = new_username
        if new_password:
            user.password = new_password
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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

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

    # Kalender und andere Daten an das Template übergeben
    return render_template('dashboard.html', events=events, tasks=tasks, now=datetime.now(), month_calendar=month_calendar)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)