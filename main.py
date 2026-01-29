import sqlite3

DB_NAME = "database.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        major TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        instructor TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_courses (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_id) REFERENCES courses(course_id)
    )
    """)

    conn.commit()
    conn.close()


def add_student():
    name = input("Ім'я: ")
    age = int(input("Вік: "))
    major = input("Спеціальність: ")

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
        (name, age, major)
    )
    conn.commit()
    conn.close()
    print("Студента додано")


def add_course():
    name = input("Назва курсу: ")
    instructor = input("Викладач: ")

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO courses (course_name, instructor) VALUES (?, ?)",
        (name, instructor)
    )
    conn.commit()
    conn.close()
    print("Курс додано")


def show_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        print(row)
    conn.close()


def show_courses():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    for row in cur.fetchall():
        print(row)
    conn.close()

def register_student_to_course():
    student_id = int(input("ID студента: "))
    course_id = int(input("ID курсу: "))

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",
        (student_id, course_id)
    )
    conn.commit()
    conn.close()
    print("Студента зареєстровано на курс")


def show_students_on_course():
    course_id = int(input("ID курсу: "))

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT students.id, students.name
        FROM students
        JOIN student_courses ON students.id = student_courses.student_id
        WHERE student_courses.course_id = ?
    """, (course_id,))

    students = cur.fetchall()
    if not students:
        print("На курсі немає студентів")
    else:
        for s in students:
            print(s)

    conn.close()


def main():
    create_tables()

    while True:
        print("\n1. Додати нового студента")
        print("2. Додати новий курс")
        print("3. Показати список студентів")
        print("4. Показати список курсів")
        print("5. Зареєструвати студента на курс")
        print("6. Показати студентів на конкретному курсі")
        print("7. Вийти")

        choice = input("Оберіть опцію (1-7): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            show_students()
        elif choice == "4":
            show_courses()
        elif choice == "5":
            register_student_to_course()
        elif choice == "6":
            show_students_on_course()
        elif choice == "7":
            print("Вихід...")
            break
        else:
            print("Некоректний вибір")


if __name__ == "__main__":
    main()