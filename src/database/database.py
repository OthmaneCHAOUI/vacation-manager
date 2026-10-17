import os
import sqlite3
import sys
from pathlib import Path
from shutil import copy2

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _get_database_path():
    if not getattr(sys, "frozen", False):
        return PROJECT_ROOT / "src" / "data" / "database.db"

    if sys.platform == "win32":
        default_data_dir = Path.home() / "AppData" / "Local"
        data_dir = Path(os.environ.get("LOCALAPPDATA") or default_data_dir)
    elif sys.platform == "darwin":
        data_dir = Path.home() / "Library" / "Application Support"
    else:
        default_data_dir = Path.home() / ".local" / "share"
        data_dir = Path(os.environ.get("XDG_DATA_HOME") or default_data_dir)

    return data_dir / "vacation-manager" / "database.db"


DB_PATH = _get_database_path()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

if getattr(sys, "frozen", False):
    legacy_db_path = PROJECT_ROOT / "src" / "data" / "database.db"
    if legacy_db_path.is_file() and not DB_PATH.exists():
        copy2(legacy_db_path, DB_PATH)


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

        columns = {
            row["name"]
            for row in cur.execute("PRAGMA table_info(vacation)").fetchall()
        }
        if "reason" not in columns:
            cur.execute("ALTER TABLE vacation ADD COLUMN reason TEXT DEFAULT ''")

        cur.execute("CREATE INDEX IF NOT EXISTS idx_vac_emp ON vacation(employee_id);")
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_vac_dates ON vacation(start_date, end_date);"
        )

        conn.commit()


# Initialize the database when this module is imported.
init_db()
