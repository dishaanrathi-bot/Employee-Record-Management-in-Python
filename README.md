## SHORT DESCRIPTION:

A command-line Employee Record Management System built in Python using SQLite database storage to add, display, and manage employee records, including employee ID, name, and salary, with duplicate ID validation.

## FEATURES:

1. Add Employee: Accepts employee ID, name, and salary and stores records in the database.
2. Display Employees: Retrieves and displays all stored employee records.
3. Duplicate ID Handling: Prevents duplicate employee IDs using SQLite integrity checks.
4. Menu-Driven Interface: Provides a simple command-line menu to add employees, view records, or exit.
5. Persistent Storage: Saves employee records in an SQLite database so they remain available after the program closes.

## DATA STRUCTURES AND TECHNOLOGIES USED:

- Classes and Objects: Uses an `Employee` class to represent employee details.
- Lists: Stores employee objects temporarily in a Python list.
- SQLite Database: Stores employee records persistently in `employees.db`.
- SQL Queries: Uses `CREATE TABLE`, `INSERT`, and `SELECT` statements to manage records.
- Exception Handling: Handles duplicate employee IDs using `sqlite3.IntegrityError`.

## DATABASE AUTOMATICALLY CREATED:

- employees.db — Stores employee records in the `Employee` table.
- Table Columns: `emp_id`, `name`, `salary`

## HOW TO RUN:

1. Make sure Python 3 is installed on your computer.
2. Save the code in a file named `main.py`.
3. Open a terminal or command prompt in the project folder.
4. Run the command:

```
python main.py
```
