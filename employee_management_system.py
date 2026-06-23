import sqlite3

# Database Connection
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
)
""")

conn.commit()


# Add Employee
def add_employee():
    name = input("Enter Name: ")
    department = input("Enter Department: ")
    salary = float(input("Enter Salary: "))

    cursor.execute("""
    INSERT INTO employees(name, department, salary)
    VALUES (?, ?, ?)
    """, (name, department, salary))

    conn.commit()

    print("Employee Added Successfully")


# View Employees
def view_employees():

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    print("\n===== Employee Records =====")

    for emp in employees:
        print(
            f"ID: {emp[0]} | "
            f"Name: {emp[1]} | "
            f"Department: {emp[2]} | "
            f"Salary: ₹{emp[3]}"
        )


# Search Employee
def search_employee():

    emp_id = int(input("Enter Employee ID: "))

    cursor.execute(
        "SELECT * FROM employees WHERE id=?",
        (emp_id,)
    )

    emp = cursor.fetchone()

    if emp:
        print("\nEmployee Found")
        print(emp)
    else:
        print("Employee Not Found")


# Update Employee Salary
def update_salary():

    emp_id = int(input("Enter Employee ID: "))
    new_salary = float(input("Enter New Salary: "))

    cursor.execute("""
    UPDATE employees
    SET salary=?
    WHERE id=?
    """, (new_salary, emp_id))

    conn.commit()

    print("Salary Updated Successfully")


# Delete Employee
def delete_employee():

    emp_id = int(input("Enter Employee ID: "))

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (emp_id,)
    )

    conn.commit()

    print("Employee Deleted Successfully")


# Department Wise Report
def department_report():

    cursor.execute("""
    SELECT department,
           COUNT(*),
           AVG(salary)
    FROM employees
    GROUP BY department
    """)

    report = cursor.fetchall()

    print("\n===== Department Report =====")

    for dept in report:
        print(
            f"Department: {dept[0]}"
            f" | Employees: {dept[1]}"
            f" | Avg Salary: ₹{round(dept[2],2)}"
        )


# Main Menu
while True:

    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Salary")
    print("5. Delete Employee")
    print("6. Department Report")
    print("7. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_salary()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        department_report()

    elif choice == "7":
        print("Exiting...")
        break

    else:
        print("Invalid Choice")

conn.close()
