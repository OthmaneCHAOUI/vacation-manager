from src.database.database import get_connection

class EmployeeModel:
    """ Data Access Object for employee-related database operations. """
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_all_employees():
        """ Returns all employees from the database. """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, first_name, last_name, position, vacation_credit, last_year_remaining, vacation_used
                FROM employee
                ORDER BY last_name ASC
                """
            )
            return cur.fetchall()

    @staticmethod
    def add_employee(first_name, last_name, position, vacation_credit=22, last_year_remaining=0, vacation_used=0):
        """Adds a new employee to the database."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO employee (first_name, last_name, position, vacation_credit, last_year_remaining, vacation_used)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    first_name,
                    last_name,
                    position,
                    vacation_credit,
                    last_year_remaining,
                    vacation_used,
                ),
            )
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def remove_employee(emp_id):
        """Removes an employee from the database."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM employee WHERE id=?", (emp_id,))
            conn.commit()

    @staticmethod
    def get_employee_by_id(emp_id):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee WHERE id=?", (emp_id,))
            return cur.fetchone()

    @staticmethod
    def update(
        emp_id,
        first_name,
        last_name,
        position,
        vacation_credit,
        last_year_remaining,
        vacation_used,
    ):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE employee
                SET first_name=?, last_name=?, position=?,
                    vacation_credit=?, last_year_remaining=?, vacation_used=?
                WHERE id=?
                """,
                (
                    first_name,
                    last_name,
                    position,
                    vacation_credit,
                    last_year_remaining,
                    vacation_used,
                    emp_id,
                ),
            )
            conn.commit()

    @staticmethod
    def update_vacation_used(emp_id, used_days):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE employee SET vacation_used=? WHERE id=?",
                (used_days, emp_id),
            )
            conn.commit()