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
                SELECT v.id, v.employee_id, e.first_name, e.last_name, v.start_date, v.end_date, v.reason, v.status, v.created_at
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
        if not vacation_ids:
            return
        with get_connection() as conn:
            cur = conn.cursor()
            placeholders = ",".join(["?"] * len(vacation_ids))
            cur.execute(
                f"DELETE FROM vacation WHERE id IN ({placeholders})", vacation_ids
            )
            conn.commit()

    @staticmethod
    def get_employee_ids_for_vacations(vacation_ids):
        """Return employee IDs associated with vacation IDs."""
        if not vacation_ids:
            return []
        with get_connection() as conn:
            cur = conn.cursor()
            placeholders = ",".join(["?"] * len(vacation_ids))
            cur.execute(
                f"SELECT DISTINCT employee_id FROM vacation WHERE id IN ({placeholders})",
                vacation_ids,
            )
            return [row["employee_id"] for row in cur.fetchall()]

    @staticmethod
    def get_vacations_for_employee_by_id(emp_id):
        """Returns vacation requests for a specific employee."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT v.start_date, v.end_date, v.created_at
                FROM vacation v
                WHERE v.employee_id = ?
                ORDER BY v.created_at DESC
                """,
                (emp_id,),
            )
            return cur.fetchall()

    @staticmethod
    def get_all_employees_with_vacation():
        """Returns employees with vacation requests."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT DISTINCT e.id, e.first_name, e.last_name
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                ORDER BY e.last_name ASC, e.first_name ASC
                """
            )
            return cur.fetchall()
