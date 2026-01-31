import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup Database: This creates a file named 'project.db' in your folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'project.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- The Database Model ---
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


# Create the database file (runs only if file doesn't exist)
with app.app_context():
    db.create_all()


# --- Updated Routes ---
@app.route('/')
def index():
    todo_list = Todo.query.all()  # Fetch all tasks from DB
    return render_template('index.html', todos=todo_list)


@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('todo')
    if task_text:
        new_todo = Todo(task=task_text)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/check/<int:todo_id>')
def check(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
