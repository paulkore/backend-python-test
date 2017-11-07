from flask import g
from common import empty


class User:
    id = None
    username = None
    # password is not included on this object for security reasons

    def __init__(self, row):
        self.id = row['id']
        self.username = row['username']

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }


class Todo:
    id = None
    user_id = None
    description = None
    completed = None

    def __init__(self, row):
        self.id = row['id']
        self.user_id = row['user_id']
        self.description = row['description']
        self.completed = True if row['completed'] else False

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'completed': self.completed,
        }


def find_user(username, password):
    if empty(username):
        raise ValueError('username must be provided')
    if empty(password):
        raise ValueError('password must be provided')

    sql = "SELECT id, username FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    row = cur.fetchone()
    if not row:
        return None
    return User(row)


def find_todos(user_id):
    if user_id is None:
        raise ValueError('user_id must be provided')

    cur = g.db.execute("SELECT * FROM todos WHERE user_id = '%s'" % user_id)
    rows = cur.fetchall()

    return list(map((lambda row: Todo(row)), rows))


def find_todo(user_id, todo_id):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if todo_id is None:
        raise ValueError('todo_id must be provided')

    cur = g.db.execute("SELECT * FROM todos WHERE id = '%s' AND user_id = '%s'" % (todo_id, user_id))
    row = cur.fetchone()
    if not row:
        return None

    return Todo(row)


def create_todo(user_id, description):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if empty(description):
        raise ValueError('description must be provided')

    g.db.execute("INSERT INTO todos (user_id, description) VALUES ('%s', '%s')" % (user_id, description))
    g.db.commit()


def delete_todo(user_id, todo_id):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if todo_id is None:
        raise ValueError('todo_id must be provided')

    g.db.execute("DELETE FROM todos WHERE id = '%s' AND user_id = '%s'" % (todo_id, user_id))
    g.db.commit()


def mark_completed(user_id, todo_id):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if todo_id is None:
        raise ValueError('todo_id must be provided')

    g.db.execute("UPDATE todos SET completed=1 WHERE id = '%s' AND user_id = '%s'" % (todo_id, user_id))
    g.db.commit()
