import tkinter as tk
from tkinter import messagebox
import sqlite3

# DB setup
def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        roll INTEGER PRIMARY KEY,
        name TEXT,
        course TEXT,
        marks INTEGER
    )
    """)
    conn.commit()
    conn.close()

# Functions
def add_student():
    roll = entry_roll.get()
    name = entry_name.get()
    course = entry_course.get()
    marks = entry_marks.get()

    if not (roll and name and course and marks):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        conn = sqlite3.connect("students.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (roll, name, course, marks))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        view_students()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")

def view_students():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        listbox.insert(tk.END, row)

def delete_student():
    roll = entry_roll.get()
    if not roll:
        messagebox.showwarning("Input Error", "Roll number required!")
        return
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Student record deleted!")
    clear_fields()
    view_students()

def update_student():
    roll = entry_roll.get()
    name = entry_name.get()
    course = entry_course.get()
    marks = entry_marks.get()

    if not (roll and name and course and marks):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, course=?, marks=? WHERE roll=?", (name, course, marks, roll))
    conn.commit()
    conn.close()
    messagebox.showinfo("Updated", "Student details updated!")
    clear_fields()
    view_students()

def search_student():
    roll = entry_roll.get()
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE roll=?", (roll,))
    row = cur.fetchone()
    conn.close()
    listbox.delete(0, tk.END)
    if row:
        listbox.insert(tk.END, row)
    else:
        messagebox.showinfo("Not Found", "Student not found.")

def clear_fields():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_marks.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x500")

tk.Label(root, text="Roll No").grid(row=0, column=0)
entry_roll = tk.Entry(root)
entry_roll.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Course").grid(row=2, column=0)
entry_course = tk.Entry(root)
entry_course.grid(row=2, column=1)

tk.Label(root, text="Marks").grid(row=3, column=0)
entry_marks = tk.Entry(root)
entry_marks.grid(row=3, column=1)

tk.Button(root, text="Add", command=add_student).grid(row=4, column=0)
tk.Button(root, text="View All", command=view_students).grid(row=4, column=1)
tk.Button(root, text="Delete", command=delete_student).grid(row=5, column=0)
tk.Button(root, text="Update", command=update_student).grid(row=5, column=1)
tk.Button(root, text="Search", command=search_student).grid(row=6, column=0)
tk.Button(root, text="Clear", command=clear_fields).grid(row=6, column=1)

listbox = tk.Listbox(root, width=50)
listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

init_db()
view_students()
root.mainloop()
