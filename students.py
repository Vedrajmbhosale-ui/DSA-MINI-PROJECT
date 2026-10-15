
import tkinter as tk
from tkinter import messagebox
import json
import os


# Student Database using Hashing
class StudentDatabase:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.filename = "students.json"
        self.load_data()

    # Hash function
    def hash_function(self, roll_no):
        return int(roll_no) % self.size

    # Add or update student
    def insert(self, roll_no, name, course, marks):
        index = self.hash_function(roll_no)

        for student in self.table[index]:
            if student["roll_no"] == roll_no:
                student["name"] = name
                student["course"] = course
                student["marks"] = marks
                self.save_data()
                return "Student record updated successfully!"

        self.table[index].append({
            "roll_no": roll_no,
            "name": name,
            "course": course,
            "marks": marks
        })

        self.save_data()
        return "Student added successfully!"

    # Search student
    def search(self, roll_no):
        index = self.hash_function(roll_no)

        for student in self.table[index]:
            if student["roll_no"] == roll_no:
                return student

        return None

    # Delete student
    def delete(self, roll_no):
        index = self.hash_function(roll_no)

        for student in self.table[index]:
            if student["roll_no"] == roll_no:
                self.table[index].remove(student)
                self.save_data()
                return True

        return False

    # Display all students
    def display(self):
        students = []
        for bucket in self.table:
            students.extend(bucket)
        return students

    # Save records to JSON file
    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.display(), file, indent=4)

    # Load records from JSON file
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    students = json.load(file)

                for student in students:
                    index = self.hash_function(student["roll_no"])
                    self.table[index].append(student)

            except (json.JSONDecodeError, KeyError, TypeError):
                messagebox.showwarning(
                    "Warning",
                    "Existing student data could not be loaded."
                )


# Create database object
db = StudentDatabase()


# GUI functions
def add_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    marks = marks_entry.get().strip()

    if not roll or not name or not course or not marks:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        roll = int(roll)
        marks = float(marks)

        if roll < 0 or not 0 <= marks <= 100:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Roll number must be non-negative and marks must be 0-100."
        )
        return

    result = db.insert(roll, name, course, marks)
    messagebox.showinfo("Success", result)
    clear_fields()
    display_students()


def search_student():
    roll = roll_entry.get().strip()

    try:
        roll = int(roll)
        if roll < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid roll number.")
        return

    student = db.search(roll)

    if student:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, student["name"])

        course_entry.delete(0, tk.END)
        course_entry.insert(0, student["course"])

        marks_entry.delete(0, tk.END)
        marks_entry.insert(0, str(student["marks"]))

        messagebox.showinfo("Found", "Student record found!")
    else:
        messagebox.showinfo("Not Found", "Student not found.")


def update_student():
    add_student()


def delete_student():
    try:
        roll = int(roll_entry.get().strip())
        if roll < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid roll number.")
        return

    if db.delete(roll):
        messagebox.showinfo("Success", "Student deleted successfully!")
        clear_fields()
        display_students()
    else:
        messagebox.showinfo("Not Found", "Student not found.")


def display_students():
    output.delete("1.0", tk.END)

    students = sorted(db.display(), key=lambda s: s["roll_no"])

    if not students:
        output.insert(tk.END, "No student records available.")
        return

    output.insert(
        tk.END,
        f"{'Roll No':<12}{'Name':<20}{'Course':<15}{'Marks':<10}\n"
    )
    output.insert(tk.END, "-" * 60 + "\n")

    for student in students:
        output.insert(
            tk.END,
            f"{student['roll_no']:<12}"
            f"{student['name']:<20}"
            f"{student['course']:<15}"
            f"{student['marks']:<10}\n"
        )


def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


# Create GUI window
root = tk.Tk()
root.title("Student Database Management System Using Hashing")
root.geometry("750x600")
root.configure(bg="#eaf2f8")

tk.Label(
    root,
    text="STUDENT DATABASE MANAGEMENT SYSTEM",
    font=("Arial", 16, "bold"),
    bg="#eaf2f8"
).pack(pady=12)

# Input frame
frame = tk.Frame(root, bg="#eaf2f8")
frame.pack(pady=5)

tk.Label(frame, text="Roll Number:", bg="#eaf2f8").grid(
    row=0, column=0, padx=10, pady=6, sticky="w"
)
roll_entry = tk.Entry(frame, width=30)
roll_entry.grid(row=0, column=1, pady=6)

tk.Label(frame, text="Student Name:", bg="#eaf2f8").grid(
    row=1, column=0, padx=10, pady=6, sticky="w"
)
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=1, column=1, pady=6)

tk.Label(frame, text="Course:", bg="#eaf2f8").grid(
    row=2, column=0, padx=10, pady=6, sticky="w"
)
course_entry = tk.Entry(frame, width=30)
course_entry.grid(row=2, column=1, pady=6)

tk.Label(frame, text="Marks:", bg="#eaf2f8").grid(
    row=3, column=0, padx=10, pady=6, sticky="w"
)
marks_entry = tk.Entry(frame, width=30)
marks_entry.grid(row=3, column=1, pady=6)

# Buttons
buttons = tk.Frame(root, bg="#eaf2f8")
buttons.pack(pady=12)

tk.Button(
    buttons, text="Add Student", width=14,
    command=add_student
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    buttons, text="Search Student", width=14,
    command=search_student
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    buttons, text="Update Student", width=14,
    command=update_student
).grid(row=0, column=2, padx=5, pady=5)

tk.Button(
    buttons, text="Delete Student", width=14,
    command=delete_student
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    buttons, text="Display All", width=14,
    command=display_students
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    buttons, text="Clear Fields", width=14,
    command=clear_fields
).grid(row=1, column=2, padx=5, pady=5)

# Output area
tk.Label(
    root,
    text="Student Records",
    font=("Arial", 12, "bold"),
    bg="#eaf2f8"
).pack(pady=5)

output = tk.Text(root, height=12, width=85, font=("Courier", 10))
output.pack(padx=15, pady=5)

display_students()

# Start application
root.mainloop()
