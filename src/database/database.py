import os
import sqlite3
import sys
from pathlib import Path
from shutil import copy2


class Database:
    """Manage the SQLite database connection and initialization."""

    def __init__(self, db_path=None):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        if self.connection is None:
            if self.db_path is None:
                self.db_path = self.get_database_path()
                self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    @staticmethod
    def get_database_path():
        """Determine the appropriate database path based on the execution context."""
        if not getattr(sys, "frozen", False):
            return Path(__file__).resolve().parents[2] / "src" / "data" / "database.db"

        if sys.platform == "win32":
            default_data_dir = Path.home() / "AppData" / "Local"
            data_dir = Path(os.environ.get("LOCALAPPDATA") or default_data_dir)
        elif sys.platform == "darwin":
            data_dir = Path.home() / "Library" / "Application Support"
        else:
            default_data_dir = Path.home() / ".local" / "share"
            data_dir = Path(os.environ.get("XDG_DATA_HOME") or default_data_dir)

        return data_dir / "vacation-manager" / "database.db"

    def close(self):
        """Close the database connection, if one is open."""
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def create_schema(self):
        """Create the database schema if it does not exist."""
        with self.connect() as conn:
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

    def initialize_database(self):
        """Initialize the database, creating the schema if necessary."""
        if self.db_path is None:
            self.db_path = self.get_database_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        if getattr(sys, "frozen", False):
            legacy_db_path = Path(__file__).resolve().parents[2] / "src" / "data" / "database.db"
            if legacy_db_path.is_file() and not self.db_path.exists():
                copy2(legacy_db_path, self.db_path)

        self.create_schema()


DB_PATH = Database.get_database_path()
_database = Database(DB_PATH)
_database.initialize_database()


def get_connection():
    """Return the shared SQLite connection with column-name access."""
    return _database.connect()


def init_db():
    """Create the database tables and indexes if they do not exist."""
    if not DB_PATH.exists():
        _database.close()
        _database.db_path = DB_PATH
    _database.create_schema()