import sys
from pathlib import Path
import sqlite3
from PyQt5.QtWidgets import QApplication
from src.view.home_view import HomeView
from src.model.database import init_db, DB_PATH


def check_database():
    """Check if DB file is valid. If corrupted, remove it."""
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("PRAGMA integrity_check;")
            conn.close()
        except sqlite3.DatabaseError:
            print("Database corrupted. Removing and recreating...")
            DB_PATH.unlink()
    init_db()


def main():
    check_database()
    app = QApplication(sys.argv)
    window = HomeView()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
