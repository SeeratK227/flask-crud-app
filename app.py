from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database URI. Using SQLite file-based DB here
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'

with app.app_context():
    print("Creating database tables if they do not exist...")
    db.create_all()

# Extend your app to filter tasks (e.g., show only completed tasks).

@app.route("/")
def index():
    filter_type = request.args.get("filter")

    if filter_type == "completed":
        tasks = Task.query.filter_by(completed=True).all()
    elif filter_type == "uncompleted":
        tasks = Task.query.filter_by(completed=False).all()
    else:
        tasks = Task.query.all()

    return render_template("index.html", tasks=tasks, filter_type=filter_type)



@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)