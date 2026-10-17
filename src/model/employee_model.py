from src.database.database import get_connection


class EmployeeModel:
    """Model for employee CRUD operations."""

    @staticmethod
    def get_all():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee ORDER BY id DESC")
            return cur.fetchall()

    @staticmethod
    def get_by_id(emp_id):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee WHERE id=?", (emp_id,))
            return cur.fetchone()

    @staticmethod
    def create(
        first_name, last_name, position, vacation_credit=22, last_year_remaining=0
    ):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO employee (first_name, last_name, position, vacation_credit, last_year_remaining)
                VALUES (?, ?, ?, ?, ?)
                """,
                (first_name, last_name, position, vacation_credit, last_year_remaining),
            )
            conn.commit()
            return cur.lastrowid

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

    @staticmethod
    def delete(emp_id):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM employee WHERE id=?", (emp_id,))
            conn.commit()
