import sqlite3
from datetime import date

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    date TEXT,
    status TEXT
)
""")

conn.commit()

while True:

    print("\n1.Mark Attendance")
    print("2.View Attendance")
    print("3.Exit")

    choice = input("Choice: ")

    if choice == "1":

        name = input("Student Name: ")

        status = input(
            "Present/Absent: "
        )

        cursor.execute("""
        INSERT INTO attendance
        (student,date,status)
        VALUES(?,?,?)
        """, (
            name,
            str(date.today()),
            status
        ))

        conn.commit()

    elif choice == "2":

        cursor.execute(
            "SELECT * FROM attendance"
        )

        for row in cursor.fetchall():
            print(row)

    elif choice == "3":
        break

conn.close()
