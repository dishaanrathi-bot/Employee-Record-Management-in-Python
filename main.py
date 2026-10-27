import sqlite3
import hashlib
import secrets
import csv
import math
from datetime import datetime
from getpass import getpass

DB = "employee.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    email TEXT NOT NULL,
    contact TEXT NOT NULL,
    salary REAL NOT NULL CHECK(salary >= 0)
)
""")
conn.commit()

FIELDS = """
employee_id, name, department, designation,
email, contact, salary
"""


# ---------- PASSWORD SECURITY ----------
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(),
        bytes.fromhex(salt), 200000
    ).hex()


# ---------- INPUT VALIDATION ----------
def get_text(prompt, old=None):
    while True:
        value = input(prompt).strip()
        if old is not None and value == "":
            return old
        if value:
            return value
        print("This field cannot be empty.")


def get_email(old=None):
    while True:
        value = input("Email: ").strip().lower()
        if old is not None and value == "":
            return old
        if value.count("@") == 1:
            name, domain = value.split("@")
            if name and "." in domain and not domain.startswith("."):
                return value
        print("Enter a valid email address.")


def get_contact(old=None):
    while True:
        value = input("Contact (10 digits): ").strip()
        if old is not None and value == "":
            return old
        if value.isdigit() and len(value) == 10:
            return value
        print("Contact must contain exactly 10 digits.")


def get_salary(old=None):
    while True:
        value = input("Salary: ").strip()
        if old is not None and value == "":
            return old
        try:
            amount = float(value)
            if math.isfinite(amount) and amount >= 0:
                return amount
        except ValueError:
            pass
        print("Enter a valid non-negative salary.")


# ---------- CREATE ACCOUNT ----------
def create_account():
    print("\n--- CREATE EMPLOYEE ACCOUNT ---")
    emp_id = get_text("Choose Employee ID: ")

    exists = cur.execute(
        "SELECT 1 FROM employees WHERE employee_id=?",
        (emp_id,)
    ).fetchone()

    if exists:
        print("Employee ID already exists. Choose another ID.")
        return

    while True:
        password = getpass("Create password (minimum 6 characters): ")
        if len(password) >= 6:
            confirm = getpass("Confirm password: ")
            if password == confirm:
                break
            print("Passwords do not match.")
        else:
            print("Password must contain at least 6 characters.")

    name = get_text("Full name: ")
    department = get_text("Department: ")
    designation = get_text("Designation: ")
    email = get_email()
    contact = get_contact()
    salary = get_salary()

    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    cur.execute("""
        INSERT INTO employees
        (employee_id, name, password_hash, salt,
         department, designation, email, contact, salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        emp_id, name, password_hash, salt,
        department, designation, email, contact, salary
    ))
    conn.commit()
    print("Account created successfully! You can now log in.")


# ---------- LOGIN ----------
def login():
    print("\n--- EMPLOYEE LOGIN ---")
    emp_id = input("Employee ID: ").strip()
    password = getpass("Password: ")

    employee = cur.execute(
        "SELECT * FROM employees WHERE employee_id=?",
        (emp_id,)
    ).fetchone()

    if employee and secrets.compare_digest(
        hash_password(password, employee["salt"]),
        employee["password_hash"]
    ):
        print("Login successful. Welcome,", employee["name"])
        return emp_id

    print("Invalid Employee ID or password.")
    return None


# ---------- DISPLAY EMPLOYEE ----------
def show_employee(emp):
    print("-" * 40)
    print("Employee ID :", emp["employee_id"])
    print("Name        :", emp["name"])
    print("Department  :", emp["department"])
    print("Designation :", emp["designation"])
    print("Email       :", emp["email"])
    print("Contact     :", emp["contact"])
    print("Salary      : Rs.", format(emp["salary"], ".2f"))


def get_employee(emp_id):
    return cur.execute(
        f"SELECT {FIELDS} FROM employees WHERE employee_id=?",
        (emp_id,)
    ).fetchone()


# ---------- DSA: SINGLY LINKED LIST ----------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        node = Node(data)
        if self.head is None:
            self.head = node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def display(self):
        current = self.head
        if current is None:
            print("No employee records found.")
        while current:
            show_employee(current.data)
            current = current.next

    def search(self, keyword):
        results = []
        current = self.head
        keyword = keyword.lower()

        while current:
            emp = current.data
            if (keyword in emp["employee_id"].lower()
                    or keyword in emp["name"].lower()):
                results.append(emp)
            current = current.next
        return results


def load_employees():
    records = cur.execute(
        f"SELECT {FIELDS} FROM employees"
    ).fetchall()

    linked_list = LinkedList()
    for emp in records:
        linked_list.append(emp)
    return linked_list


# ---------- VIEW AND SEARCH ----------
def view_employees():
    print("\n--- EMPLOYEE DIRECTORY ---")
    load_employees().display()


def search_employee():
    keyword = input("Enter Employee ID or name: ").strip()
    if not keyword:
        print("Search value cannot be empty.")
        return

    results = load_employees().search(keyword)
    if results:
        for emp in results:
            show_employee(emp)
    else:
        print("No matching employee found.")


# ---------- UPDATE OWN DETAILS ----------
def update_details(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        print("Your account was not found.")
        return

    print("Press Enter to keep the current value.")
    name = get_text(f"Name [{emp['name']}]: ", emp["name"])
    department = get_text(
        f"Department [{emp['department']}]: ", emp["department"]
    )
    designation = get_text(
        f"Designation [{emp['designation']}]: ", emp["designation"]
    )
    email = get_email(emp["email"])
    contact = get_contact(emp["contact"])
    salary = get_salary(emp["salary"])

    cur.execute("""
        UPDATE employees
        SET name=?, department=?, designation=?,
            email=?, contact=?, salary=?
        WHERE employee_id=?
    """, (
        name, department, designation,
        email, contact, salary, emp_id
    ))
    conn.commit()
    print("Your details have been updated.")


# ---------- DELETE OWN ACCOUNT ----------
def delete_account(emp_id):
    confirm = input(
        "Permanently delete your account? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        cur.execute(
            "DELETE FROM employees WHERE employee_id=?",
            (emp_id,)
        )
        conn.commit()
        print("Your account has been deleted.")
        return True

    print("Deletion cancelled.")
    return False


# ---------- SORTING ----------
def sort_employees():
    records = cur.execute(
        f"SELECT {FIELDS} FROM employees"
    ).fetchall()

    if not records:
        print("No employee records to sort.")
        return

    print("1. Employee ID (ascending)")
    print("2. Salary (low to high)")
    print("3. Salary (high to low)")
    choice = input("Choose: ").strip()

    if choice == "1":
        records = sorted(
            records, key=lambda e: e["employee_id"].lower()
        )
    elif choice == "2":
        records = sorted(records, key=lambda e: e["salary"])
    elif choice == "3":
        records = sorted(
            records, key=lambda e: e["salary"], reverse=True
        )
    else:
        print("Invalid choice.")
        return

    for emp in records:
        show_employee(emp)


# ---------- REPORTS ----------
def employee_report():
    report = cur.execute("""
        SELECT COUNT(*) AS total,
               COALESCE(SUM(salary), 0) AS total_salary,
               COALESCE(AVG(salary), 0) AS avg_salary,
               COALESCE(MIN(salary), 0) AS min_salary,
               COALESCE(MAX(salary), 0) AS max_salary
        FROM employees
    """).fetchone()

    print("\n======= EMPLOYEE REPORT =======")
    print("Generated:", datetime.now().strftime("%d-%m-%Y %H:%M"))
    print("Total employees:", report["total"])
    print("Total salary: Rs.", round(report["total_salary"], 2))
    print("Average salary: Rs.", round(report["avg_salary"], 2))
    print("Lowest salary: Rs.", round(report["min_salary"], 2))
    print("Highest salary: Rs.", round(report["max_salary"], 2))

    print("\nDepartment-wise count:")
    departments = cur.execute("""
        SELECT department, COUNT(*) AS total
        FROM employees GROUP BY department
        ORDER BY department
    """).fetchall()

    for row in departments:
        print(row["department"], ":", row["total"])

    choice = input("\nExport directory to CSV? (y/n): ").strip().lower()
    if choice == "y":
        records = cur.execute(
            f"SELECT {FIELDS} FROM employees ORDER BY employee_id"
        ).fetchall()

        with open("employee_report.csv", "w",
                  newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Employee ID", "Name", "Department", "Designation",
                "Email", "Contact", "Salary"
            ])
            for emp in records:
                writer.writerow(list(emp))

        print("Report saved as employee_report.csv")


# ---------- EMPLOYEE DASHBOARD ----------
def dashboard(emp_id):
    while True:
        print("\n======= EMPLOYEE DASHBOARD =======")
        print("1. View My Details")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update My Details")
        print("5. Delete My Account")
        print("6. Sort Employees")
        print("7. Employee Reports")
        print("8. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            emp = get_employee(emp_id)
            if emp:
                show_employee(emp)
            else:
                print("Account not found.")

        elif choice == "2":
            view_employees()

        elif choice == "3":
            search_employee()

        elif choice == "4":
            update_details(emp_id)

        elif choice == "5":
            if delete_account(emp_id):
                return

        elif choice == "6":
            sort_employees()

        elif choice == "7":
            employee_report()

        elif choice == "8":
            print("Logged out successfully.")
            return

        else:
            print("Invalid choice. Try again.")


# ---------- MAIN MENU ----------
def main():
    while True:
        print("\n===== EMPLOYEE RECORD MANAGEMENT =====")
        print("1. Create Employee Account")
        print("2. Employee Login")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            create_account()

        elif choice == "2":
            emp_id = login()
            if emp_id:
                dashboard(emp_id)

        elif choice == "0":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped.")
    finally:
        conn.close()
