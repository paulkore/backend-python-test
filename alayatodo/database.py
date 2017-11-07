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


PAGE_SIZE = 10


def find_user(username, password):
    if empty(username):
        raise ValueError('username must be provided')
    if empty(password):
        raise ValueError('password must be provided')

    cur = g.db.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", [username, password])
    row = cur.fetchone()
    if not row:
        return None
    return User(row)


def get_todos_page_count(user_id):
    if user_id is None:
        raise ValueError('user_id must be provided')

    cur = g.db.execute("SELECT count(*) as count FROM todos where user_id = ?", [user_id])
    count = cur.fetchone()['count']
    return count / PAGE_SIZE + (1 if count % PAGE_SIZE else 0)


def find_todos(user_id, page):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if page is None or page < 0:
        raise ValueError('page must be a number greater than zero')

    cur = g.db.execute("SELECT * FROM todos WHERE user_id = ? LIMIT ? OFFSET ?", [user_id, PAGE_SIZE, PAGE_SIZE * (page-1)])
    rows = cur.fetchall()

    return list(map((lambda row: Todo(row)), rows))


def find_todo(user_id, todo_id):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if todo_id is None:
        raise ValueError('todo_id must be provided')

    cur = g.db.execute("SELECT * FROM todos WHERE id = ? AND user_id = ?", [todo_id, user_id])
    row = cur.fetchone()
    if not row:
        return None

    return Todo(row)


def create_todo(user_id, description):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if empty(description):
        raise ValueError('description must be provided')

    g.db.execute("INSERT INTO todos (user_id, description, completed) VALUES (?, ?, ?)", [user_id, description, 0])
    g.db.commit()


def delete_todo(user_id, todo_id):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if todo_id is None:
        raise ValueError('todo_id must be provided')

    g.db.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", [todo_id, user_id])
    g.db.commit()


def mark_completed(user_id, todo_id):
    if user_id is None:
        raise ValueError('user_id must be provided')
    if todo_id is None:
        raise ValueError('todo_id must be provided')

    g.db.execute("UPDATE todos SET completed=1 WHERE id = ? AND user_id = ?", [todo_id, user_id])
    g.db.commit()
