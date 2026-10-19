from src.database.database import get_connection

class VacationModel:
    """Data Access Object for vacation-related database operations."""

    def __init__(self):
        pass

    @staticmethod
    def get_all_vacations():
        """ Returns all vacation requests with employee details. """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT v.id, e.first_name || ' ' || e.last_name AS employee_name, v.start_date, v.end_date, v.reason, v.status
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                ORDER BY v.start_date DESC
                """
            )
            return cur.fetchall()

    @staticmethod
    def add_vacation(employee_id, start_date, end_date, reason="", status="pending"):
        """Adds a new vacation request."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO vacation (employee_id, start_date, end_date, reason, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (employee_id, start_date, end_date, reason, status),
            )
            conn.commit()

    @staticmethod
    def remove_vacations(vacation_ids):
        """Deletes one or more vacation requests by ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            placeholders = ",".join(["?"] * len(vacation_ids))
            cur.execute(
                f"DELETE FROM vacation WHERE id IN ({placeholders})", vacation_ids
            )
            conn.commit()

    @staticmethod
    def get_vacations_for_employee_by_id(emp_id):
        """Returns vacation requests for a specific employee."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT v.start_date, v.end_date, v.created_at
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                WHERE e.id = ?
                ORDER BY v.created_at DESC
                """,
                (emp_id,),
            )
            return cur.fetchall()

    @staticmethod
    def get_vacations_for_employee_by_name(emp_name):
        """Returns vacation requests for a specific employee name."""
        with get_connection() as conn:
            cur = conn.cursor()
            first, last = emp_name.split(" ", 1)
            cur.execute(
                """
                SELECT v.start_date, v.end_date, v.created_at
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                WHERE e.first_name = ? AND e.last_name = ?
                ORDER BY v.created_at DESC
                """,
                (first, last),
            )
            return cur.fetchall()

    @staticmethod
    def get_all_employees_with_vacation():
        """Returns a list of all employees who have a vacation request."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT DISTINCT e.first_name || ' ' || e.last_name AS name
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                """
            )
            return [row["name"] for row in cur.fetchall()]

    @staticmethod
    def get_vacation_by_id(vacation_id):
        """Returns a specific vacation request by ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM vacation WHERE id = ?
                """,
                (vacation_id,),
            )
            return cur.fetchone()
