from alayatodo import app
from flask import (
    redirect,
    render_template,
    request,
    session,
)

from database import (
    find_user,
    find_todos,
    find_todo,
    create_todo,
    delete_todo,
)

from alerts import *


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = find_user(username, password)
    if user:
        session['user'] = user.to_dict()
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not logged_in():
        return redirect('/login')
    todo = find_todo(user_id(), id)
    if not todo:
        return redirect('/todo')
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>/json', methods=['GET'])
def todo_JSON(id):
    if not logged_in():
        return redirect('/login')
    todo = find_todo(user_id(), id)
    if not todo:
        return redirect('/todo')
    return render_template('todo_json.html', todo=todo.to_dict())


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not logged_in():
        return redirect('/login')

    todos = find_todos(user_id())
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not logged_in():
        return redirect('/login')

    description = request.form.get('description', '')
    if not description.strip():
        alert_warning(u'Please enter a description')
        return redirect('/todo')

    create_todo(user_id(), description)
    alert_success(u'TODO record created')
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not logged_in():
        return redirect('/login')

    delete_todo(user_id(), id)
    alert_success(u'TODO record deleted')
    return redirect('/todo')


def logged_in():
    return session['logged_in']


def user_id():
    return session['user']['id']
