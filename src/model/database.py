# src/model/database.py
import sqlite3
from pathlib import Path

# Résolution du chemin du projet (workless/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "src" / "data" / "database.db"

# Crée le répertoire si nécessaire
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Retourne une connexion sqlite3 (row_factory pour accès par nom)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crée les tables si elles n'existent pas."""
    with get_connection() as conn:
        cur = conn.cursor()

        # Table employee : firstname/lastname, position, crédit des vacances, reste de l'année précédente, utilisé cette année
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                position TEXT,
                vacation_credit INTEGER DEFAULT 22,       -- crédit pour l'année en cours
                last_year_remaining INTEGER DEFAULT 0,   -- jours reportés depuis l'année précédente
                vacation_used INTEGER DEFAULT 0,         -- jours déjà pris cette année
                created_at TEXT DEFAULT (date('now'))
            );
            """
        )

        # Table vacation : pour stocker les demandes/absences (utilisée ailleurs)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,   -- format ISO YYYY-MM-DD
                end_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',  -- pending|approved|rejected
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (employee_id) REFERENCES employee(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );
            """
        )

        # Index utiles
        cur.execute("CREATE INDEX IF NOT EXISTS idx_vac_emp ON vacation(employee_id);")
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_vac_dates ON vacation(start_date, end_date);"
        )

        conn.commit()


# Initialisation automatique au premier import
init_db()
