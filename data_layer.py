"""DATA LAYER: the only module that touches the database."""
import sqlite3

DB = "students.db"

def _conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init():
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            year INTEGER NOT NULL,
            created TEXT DEFAULT CURRENT_TIMESTAMP)""")

def insert(reg_no, name, course, year):
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO students(reg_no, name, course, year) VALUES (?, ?, ?, ?)",
            (reg_no, name, course, year))
        return cur.lastrowid

def fetch_all():
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM students ORDER BY id DESC")]

def find_by_reg_no(reg_no):
    with _conn() as c:
        r = c.execute("SELECT * FROM students WHERE reg_no = ?", (reg_no,)).fetchone()
        return dict(r) if r else None

def update(student_id, reg_no, name, course, year):
    with _conn() as c:
        return c.execute(
            "UPDATE students SET reg_no=?, name=?, course=?, year=? WHERE id=?",
            (reg_no, name, course, year, student_id)).rowcount

def delete(student_id):
    with _conn() as c:
        return c.execute("DELETE FROM students WHERE id = ?", (student_id,)).rowcount
