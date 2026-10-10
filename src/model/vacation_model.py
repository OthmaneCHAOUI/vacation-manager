from src.model.database import get_connection


class VacationModel:
    """Manages operations on the vacation table."""

    @staticmethod
    def get_all():
        """Returns all vacation requests with employee details."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT v.*, e.first_name, e.last_name
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                ORDER BY v.start_date DESC
                """
            )
            return cur.fetchall()

    @staticmethod
    def add(employee_id, start_date, end_date, reason=""):
        """Adds a new vacation request."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO vacation (employee_id, start_date, end_date, reason)
                VALUES (?, ?, ?, ?)
                """,
                (employee_id, start_date, end_date, reason),
            )
            conn.commit()

    @staticmethod
    def update_status(vacation_id, status):
        """Updates the status of a request (approved|rejected|pending)."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE vacation SET status = ?
                WHERE id = ?
                """,
                (status, vacation_id),
            )
            conn.commit()

    @staticmethod
    def delete(vacation_ids):
        """Deletes one or more vacation requests by ID."""
        with get_connection() as conn:
            cur = conn.cursor()
            placeholders = ",".join(["?"] * len(vacation_ids))
            cur.execute(
                f"DELETE FROM vacation WHERE id IN ({placeholders})", vacation_ids
            )
            conn.commit()

    @staticmethod
    def get_all_vacations():
        """Returns all vacation requests with employee details."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT v.*, e.first_name, e.last_name
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                ORDER BY v.start_date DESC
                """
            )
            return cur.fetchall()

    @staticmethod
    def get_employees_on_date(date_str):
        """Returns employees on vacation for a given date."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT e.first_name || ' ' || e.last_name AS name
                FROM vacation v
                JOIN employee e ON v.employee_id = e.id
                WHERE v.start_date <= ? AND v.end_date >= ?
                """,
                (date_str, date_str),
            )
            return [row["name"] for row in cur.fetchall()]

    @staticmethod
    def get_vacations_for_employee_by_name(emp_name):
        """Returns vacation requests for a specific employee."""
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
    def update(vac_id, start_date, end_date, status):
        """Updates a vacation request in the database."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE vacation
                SET start_date = ?, end_date = ?, status = ?
                WHERE id = ?
                """,
                (start_date, end_date, status, vac_id),
            )
            conn.commit()
