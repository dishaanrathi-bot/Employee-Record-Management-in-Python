import sqlite3

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employee (
    emp_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary REAL NOT NULL
)
""")

conn.commit()

class Employee:
    def __init__(self, emp_id, name, salary):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def display(self):
        print("ID:", self.emp_id)
        print("Name:", self.name)
        print("Salary:", self.salary)


employees = []

while True:
    print("\n--- Employee Record Management ---")
    print("1. Add Employee")
    print("2. Display Employees")
    print("3. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        emp_id = int(input("Enter Employee ID: "))
        name = input("Enter Employee Name: ")
        salary = float(input("Enter Salary: "))

        emp = Employee(emp_id, name, salary)
        employees.append(emp)

        try:
            cursor.execute("""
            INSERT INTO Employee (emp_id, name, salary)
            VALUES (?, ?, ?)
            """, (emp_id, name, salary))

            conn.commit()

            print("Employee Added!")

        except sqlite3.IntegrityError:
            print("Employee ID already exists!")

    elif choice == 2:

        cursor.execute("SELECT * FROM Employee")

        records = cursor.fetchall()

        if len(records) == 0:
            print("No Employees Found!")

        else:
            print("\n--- Employee Records ---")

            for record in records:
                emp = Employee(record[0], record[1], record[2])
                emp.display()
                print("----------------------")

    elif choice == 3:
        print("Program Ended!")

        conn.close()
        break


    else:
        print("Invalid Choice!")
