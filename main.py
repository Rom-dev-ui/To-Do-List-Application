from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Define the Task model (for request validation)
class Task(BaseModel):
    title: str
    description: str = None
    done: bool = False

# Helper functions to interact with the database
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

def add_task(task: Task):
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

# Initialize the database when the app starts
init_db()

@app.get("/tasks/")
def read_tasks():
    tasks = get_all_tasks()
    return {"tasks": tasks}

@app.post("/tasks/")
def create_task(task: Task):
    add_task(task)
    return {"message": "Task added successfully"}

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(task_id)
    return {"message": "Task deleted successfully"}
