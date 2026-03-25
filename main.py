import sqlite3

def setup_database():
    # Connect to (or create) the database file
    conn = sqlite3.connect('miva_university.db')
    cursor = conn.cursor()

    # Enable Foreign Key constraints (Critical for SQLite)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. CREATE TABLES
    cursor.executescript('''
    DROP TABLE IF EXISTS Enrollment;
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Student;
    DROP TABLE IF EXISTS Instructor;

    CREATE TABLE Student (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        date_of_birth DATE
    );

    CREATE TABLE Instructor (
        instructor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        phone_number TEXT
    );

    CREATE TABLE Course (
        course_code TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        credit_hours INTEGER,
        department TEXT NOT NULL,
        instructor_id TEXT NOT NULL,
        FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
    );

    CREATE TABLE Enrollment (
        student_id TEXT,
        course_code TEXT,
        PRIMARY KEY (student_id, course_code),
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (course_code) REFERENCES Course(course_code)
    );
    ''')

    # 2. INSERT 20 RECORDS PER TABLE (Sample Loop)
    # Adding Instructors
    instructor_names = [
        "Dr. Adaobi Okafor",
        "Prof. Samuel Ojo",
        "Dr. Chinedu Nwankwo",
        "Engr. Fatima Bello",
        "Dr. Ibrahim Suleiman",
        "Prof. Grace Akande",
        "Dr. Musa Lawal",
        "Engr. Amina Eze",
        "Dr. Peter Orekoya",
        "Prof. Eunice Adebayo",
        "Dr. Daniel Mohammed",
        "Engr. Khadija Yusuf",
        "Prof. Esther Uche",
        "Dr. Michael Okoro",
        "Engr. Shamsa Faleye",
        "Dr. Odemorin Babatunde",
        "Prof. Peace Adeniji",
        "Engr. Anthony Melah",
        "Dr. Chiamaka Nnamani",
        "Prof. Victor Amos",
    ]

    for i in range(1, 21):
        # Keep instructor_id stable (INS001..INS020) for course foreign keys.
        name = instructor_names[i - 1] if i - 1 < len(instructor_names) else f"Instructor {i}"
        cursor.execute(
            "INSERT INTO Instructor VALUES (?, ?, ?, ?)",
            (f"INS{i:03}", name, "Computer Science", f"080-{i:03}-0000"),
        )
    
    # Adding Students
    provided_students = [
        ("2024/A/CSC/0053", "Victor Amos", "victor.amos@miva.edu.ng"),
        ("2024/A/CSC/0078", "Shamsa Falola", "shamsa.falola@miva.edu.ng"),
        ("2024/A/CSC/0087", "Odemorin Babatunde", "babatunde.odemorin@miva.edu.ng"),
        ("2024/A/CSC/0083", "Esther Awoluyi", "esther.awoluyi@miva.edu.ng"),
        ("2025/A/CSC/0002", "Ejalonibu Temidayo", "temidayo.ejalonibu@miva.edu.ng"),
        ("2024/A/CSC/0054", "Peace Edet", "peace.edet@miva.edu.ng"),
        ("2024/C/CSC/0897", "Mubarak Badmus", "mubarak.badmus@miva.edu.ng"),
        ("2024/A/CSC/0134", "Peace Adeniji", "peace.adeniji@miva.edu.ng"),
        ("2024/A/CSC/0123", "Michael Olanrewaju", "michael.olanrewaju@miva.edu.ng"),
        ("2024/A/CYB/0108", "Anthony Melah", "anthony.melah@miva.edu.ng"),
        ("2025/A/CSC/0057", "Chinedu Okeke", "c.okeke8594@miva.edu.ng"),
    ]

    target_student_count = 20
    student_ids = []

    # Insert the provided students (use a fixed DOB unless your lab asks for real dates).
    for student_id, name, email in provided_students:
        cursor.execute(
            "INSERT INTO Student VALUES (?, ?, ?, ?)",
            (student_id, name, email, "2000-01-01"),
        )
        student_ids.append(student_id)

    # Fill remaining students with generated values to reach 20 rows.
    used_emails = {email for _, _, email in provided_students}
    random_first_names = [
        "Ada", "Chiamaka", "Khadija", "Samuel", "Grace",
        "Daniel", "Fatima", "Peter", "Eunice", "Amina",
    ]
    random_last_names = [
        "Okafor", "Nwankwo", "Ibrahim", "Adebayo", "Obi",
        "Eze", "Suleiman", "Musa", "Lawal", "Adamu",
    ]
    reg_start = 1001

    i = 0
    while len(student_ids) < target_student_count:
        first = random_first_names[i % len(random_first_names)]
        last = random_last_names[(i * 3) % len(random_last_names)]
        name = f"{first} {last}"

        reg_no = f"2024/A/CSC/{reg_start + i:04d}"
        # Lowercase email in the same style as your examples.
        email_local = (first + "." + last).lower()
        email = f"{email_local}@miva.edu.ng"
        if email in used_emails:
            i += 1
            continue

        cursor.execute(
            "INSERT INTO Student VALUES (?, ?, ?, ?)",
            (reg_no, name, email, "2000-01-01"),
        )
        student_ids.append(reg_no)
        used_emails.add(email)
        i += 1

    # Adding Courses (Linking to Instructors)
    # Keep Query (b) working by ensuring there's a Course row with title exactly "Database Systems".
    def normalize_course_code(code: str) -> str:
        # Convert "COS 201" -> "COS201", "MIVA-CSC 303" -> "MIVA-CSC303"
        return code.replace(" ", "")

    def infer_department(course_code: str) -> str:
        if course_code.startswith(("CSC", "MIVA-CSC", "COS", "SEN")):
            return "Computer Science"
        if course_code.startswith(("IFT", "ICT", "CYB")):
            return "Information Technology"
        if course_code.startswith(("MTH", "MIVA-MTH")):
            return "Mathematics"
        if course_code.startswith("PHY"):
            return "Physics"
        return "General Studies"

    provided_courses = [
        ("COS 201", "Computer Programming I (COS 201)"),
        ("IFT 211", "Digital Logic Design (IFT 211)"),
        ("COS 203", "Discrete Structures (COS 203)"),
        ("ENT 211", "Entrepreneurship and Innovation (ENT 211)"),
        ("SEN 201", "Introduction to Software Engineering (SEN 201)"),
        ("MTH 201", "Mathematical Methods I (MTH 201)"),
        ("CSC 299", "SIWES I (CSC 299)"),
        ("IFT 212", "Computer Architecture and Organisation (IFT 212)"),
        ("COS 202", "Computer Programming II (COS 202)"),
        ("MTH 202", "Elementary Differential Equations (MTH 202)"),
        ("PHY 202", "Introduction to Electric Circuits and Electronics (PHY 202)"),
        ("MIVA-MTH 204", "Linear Algebra II (MIVA-MTH 204)"),
        ("GST 212", "Philosophy, Logic and Human Existence (GST 212)"),
        ("MIVA-CSC 204", "Statistical Computing Inference and Modelling (MIVA-CSC 204)"),
        ("MIVA-COS 211", "Technical Certification in Computing II (MIVA-COS 211)"),
        ("GST 111", "Communication in English Language I (GST 111)"),
        ("STA 111", "Descriptive Statistics (STA 111)"),
        ("MTH 101", "Elementary Mathematics (MTH 101)"),
        ("GST 127", "Environmental Sustainability (GST 127)"),
        ("PHY 101", "General Physics I (PHY 101)"),
        ("PHY 107", "General Practical Physics (PHY 107)"),
        ("COS 101", "Introduction to Computing (COS 101)"),
        ("GST 121", "Use of Library Study Skills and ICT (GST 121)"),
        ("GST 122", "Communication in English Language II (GST 122)"),
        ("MTH 102", "Elementary Mathematics (Calculus) II (MTH 102)"),
        ("PHY 102", "General Physics II (PHY 102)"),
        ("PHY 108", "General Physics Practical II (PHY 108)"),
        ("COS 102", "Introduction to Problem-Solving (COS 102)"),
        ("MIVA-CSC 106", "Introduction to Web Technologies (MIVA-CSC 106)"),
        ("GST 112", "Nigerian Peoples and Culture (GST 112)"),
        ("MIVA-COS 111", "Technical Certification in Computing I (MIVA-COS 111)"),
        ("CSC 309", "Artificial Intelligence (CSC 309)"),
        ("ICT 305", "Data Communication System & Network (ICT 305)"),
        ("CSC 301", "Data Structures (CSC 301)"),
        ("CYB 201", "Introduction to Cybersecurity and Strategy (CYB 201)"),
        ("MIVA-CSC 303", "Introduction to Data Management (MIVA-CSC 303)"),
        ("CSC 399", "SIWES II (CSC 399)"),
    ]

    # Insert exactly 20 courses: 1 "Database Systems" + first 19 from your list.
    course_rows = [
        ("DBS101", "Database Systems", 3, "Computer Science"),
    ]

    for code, title in provided_courses[:19]:
        course_code = normalize_course_code(code)
        course_rows.append((course_code, title, 3, infer_department(course_code)))

    course_codes = []
    for i, (course_code, title, credit_hours, department) in enumerate(course_rows):
        course_codes.append(course_code)
        instructor_id = f"INS{(i % 20) + 1:03d}"  # cycle INS001..INS020
        cursor.execute(
            "INSERT INTO Course VALUES (?, ?, ?, ?, ?)",
            (course_code, title, credit_hours, department, instructor_id),
        )

    # Adding Enrollments (Linking Students to Courses)
    # One enrollment per student (20 total enrollments) distributed across the 20 courses.
    for i, student_id in enumerate(student_ids):
        course_code = course_codes[i % len(course_codes)]
        cursor.execute("INSERT INTO Enrollment VALUES (?, ?)", (student_id, course_code))

    conn.commit()
    print("✓ Database built and populated successfully.")

    # 3. RUN TESTING QUERIES
    print("\n--- Query A: Students and Enrolled Courses ---")
    cursor.execute("""SELECT Student.name, Course.title FROM Student 
                      JOIN Enrollment ON Student.student_id = Enrollment.student_id 
                      JOIN Course ON Enrollment.course_code = Course.course_code""")
    for row in cursor.fetchall(): print(row)

    print("\n--- Query B: Instructor for 'Database Systems' ---")
    cursor.execute("""SELECT Instructor.name FROM Instructor 
                      JOIN Course ON Instructor.instructor_id = Course.instructor_id 
                      WHERE Course.title = 'Database Systems'""")
    for row in cursor.fetchall():
        print(row[0])

    print("\n--- Query C: Number of Students per Course ---")
    cursor.execute("""SELECT Course.course_code, Course.title,
                      COUNT(Enrollment.student_id) AS students_enrolled
                      FROM Course
                      LEFT JOIN Enrollment ON Enrollment.course_code = Course.course_code
                      GROUP BY Course.course_code, Course.title
                      ORDER BY Course.course_code""")
    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    setup_database()