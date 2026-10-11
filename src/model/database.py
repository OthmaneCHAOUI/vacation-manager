import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "src" / "data" / "database.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Return a SQLite connection that supports column-name access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the database tables and indexes if they do not exist."""
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                position TEXT,
                vacation_credit INTEGER DEFAULT 22,       -- Current-year vacation allowance
                last_year_remaining INTEGER DEFAULT 0,   -- Days carried over from last year
                vacation_used INTEGER DEFAULT 0,         -- Days used this year
                created_at TEXT DEFAULT (date('now'))
            );
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,   -- ISO date format: YYYY-MM-DD
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',  -- pending, approved, or rejected
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (employee_id) REFERENCES employee(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );
            """
        )

        cur.execute("CREATE INDEX IF NOT EXISTS idx_vac_emp ON vacation(employee_id);")
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_vac_dates ON vacation(start_date, end_date);"
        )

        conn.commit()


# Initialize the database when this module is imported.
init_db()
