from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Event, Task
from datetime import datetime

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    events = Event.query.order_by(Event.date).all()
    tasks = Task.query.all()
    return render_template('index.html', events=events, tasks=tasks)

@routes_bp.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        description = request.form.get('description', '')
        new_event = Event(title=title, date=date, description=description)
        db.session.add(new_event)
        db.session.commit()
        flash('Event erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('add_event.html')

@routes_bp.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
        flash('Aufgabe erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('add_task.html')

@routes_bp.route('/complete_task/<int:id>')
def complete_task(id):
    task = Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
        flash('Aufgabe erledigt!', 'success')
    return redirect(url_for('routes.index'))

@routes_bp.route('/delete_event/<int:id>')
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash('Event gelöscht!', 'danger')
    return redirect(url_for('routes.index'))

@routes_bp.route('/delete_task/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Aufgabe gelöscht!', 'danger')
    return redirect(url_for('routes.index'))