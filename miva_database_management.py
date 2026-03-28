import sqlite3

def normalized_hr_db():
    conn = sqlite3.connect('miva_hr_training.db')
    cursor = conn.cursor()
    
    # Create final 5NF tables
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Departments (
        dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dept_name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Employees (
        employee_id INTEGER PRIMARY KEY,
        employee_name TEXT NOT NULL,
        dept_id INTEGER,
        FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
    );

    CREATE TABLE IF NOT EXISTS Instructors (
        instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        instructor_name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_title TEXT NOT NULL,
        instructor_id INTEGER,
        location TEXT,
        FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id)
    );

    CREATE TABLE IF NOT EXISTS Training_Records (
        employee_id INTEGER,
        course_id INTEGER,
        course_date DATE,
        PRIMARY KEY (employee_id, course_id),
        FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
        FOREIGN KEY (course_id) REFERENCES Courses(course_id)
    );
    ''')
    
    conn.commit()
    print("✓ 5NF Normalized HR Database Structure Created.")
    conn.close()

if __name__ == "__main__":
    normalized_hr_db()