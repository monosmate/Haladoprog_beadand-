from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Adatbázis modell
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.String(20), default='közepes')
    status = db.Column(db.String(20), default='folyamatban')
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'


# Adatbázis inicializálása
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    filter_status = request.args.get('status', 'all')
    filter_priority = request.args.get('priority', 'all')

    query = Task.query

    if filter_status != 'all':
        query = query.filter_by(status=filter_status)
    if filter_priority != 'all':
        query = query.filter_by(priority=filter_priority)

    tasks = query.order_by(Task.created_at.desc()).all()

    return render_template('index.html', tasks=tasks,
                           filter_status=filter_status,
                           filter_priority=filter_priority)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        priority = request.form.get('priority')
        due_date_str = request.form.get('due_date')

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass

        new_task = Task(
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date
        )

        db.session.add(new_task)
        db.session.commit()

        flash('Feladat sikeresen hozzáadva!', 'success')
        return redirect(url_for('index'))

    return render_template('add_task.html')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.category = request.form.get('category')
        task.priority = request.form.get('priority')
        task.status = request.form.get('status')

        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass

        db.session.commit()
        flash('Feladat sikeresen frissítve!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Feladat törölve!', 'info')
    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'kész'
    db.session.commit()
    flash('Feladat befejezve!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
