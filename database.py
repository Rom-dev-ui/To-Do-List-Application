import sqlite3

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    done BOOLEAN NOT NULL CHECK (done IN (0, 1)))''')
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id: int):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return task

def add_task(task):
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)', 
                 (task.title, task.description, task.done))
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
