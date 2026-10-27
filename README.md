## SHORT DESCRIPTION:

A menu-driven Employee Record Management System built in Python using SQLite database storage to create employee accounts, securely log in, view and manage employee details, search and sort records, generate salary reports, and export employee data to CSV.

## FEATURES:

1. Employee Account Management: Allows employees to create accounts and log in using their Employee ID and password.
2. View and Search Records: Displays employee details and searches records by Employee ID or name.
3. Update and Delete Account: Allows logged-in employees to update their details or permanently delete their own account.
4. Sorting and Reports: Sorts employees by ID or salary and generates salary statistics and department-wise employee counts.
5. CSV Export: Exports employee records to a CSV file for reporting and further use.
6. Input Validation and Security: Validates email, contact number, and salary inputs while securely hashing passwords with unique salts.

## DATA STRUCTURES AND TECHNOLOGIES USED:

- Classes and Objects: Uses `Node` and `LinkedList` classes to organize and search employee records.
- Singly Linked List: Stores employee records temporarily for displaying and searching.
- SQLite Database: Stores employee accounts and details persistently in `employee.db`.
- SQL Queries: Uses `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, and aggregate queries to manage records and generate reports.
- Password Security: Uses `hashlib`, `secrets`, and PBKDF2-HMAC-SHA256 for password hashing and verification.
- CSV Module: Exports employee records to a CSV file.
- Exception Handling and Validation: Handles program interruptions and validates user inputs.

## DATABASE AUTOMATICALLY CREATED:

- `employee.db` — Stores employee records in the `employees` table.
- Table Columns: `employee_id`, `name`, `password_hash`, `salt`, `department`, `designation`, `email`, `contact`, `salary`
- Export File: `employee_report.csv` — Generated when the user chooses to export the employee report.

## HOW TO RUN:

1. Make sure Python 3 is installed on your computer.
2. Save the code in a file named `main.py`.
3. Open a terminal or command prompt in the project folder.
4. Run the command:

```bash
python main.py
```

5. Create an employee account, log in, and use the dashboard menu to manage records.

## About

This project demonstrates Python programming, SQLite database management, data structures, password security, input validation, employee record handling, report generation, and CSV file operations through a simple command-line interface.
