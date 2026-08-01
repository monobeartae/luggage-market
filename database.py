"""
database.py

Handles:
- SQLite connection
- Database initialisation
- Table creation

No Telegram-related code belongs here.
"""

from pathlib import Path
import sqlite3

###############################################################################
# Database Location
###############################################################################

# project/
# ├── database.py
# └── data/
#     └── sales.db

DATABASE_DIR = Path("data")
DATABASE_FILE = DATABASE_DIR / "sales.db"


###############################################################################
# Connection
###############################################################################

def get_connection() -> sqlite3.Connection:
    """
    Returns a SQLite connection.

    Foreign key constraints are enabled automatically.
    """

    conn = sqlite3.connect(DATABASE_FILE)

    # Allows rows to behave like dictionaries.
    conn.row_factory = sqlite3.Row

    # SQLite disables foreign keys by default.
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


###############################################################################
# Database Initialisation
###############################################################################

def initialise_database() -> None:
    """
    Creates all required tables if they do not already exist.
    """

    DATABASE_DIR.mkdir(exist_ok=True)

    with get_connection() as conn:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                name TEXT NOT NULL
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS payment_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                name TEXT NOT NULL
            );
            """
        )


        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,

                payment_source_id INTEGER NOT NULL,

                sale_price REAL NOT NULL,

                sale_datetime TEXT NOT NULL,

                FOREIGN KEY (payment_source_id)
                    REFERENCES payment_sources(id)
                    ON DELETE RESTRICT
            );
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sale_id INTEGER NOT NULL,

                member_id INTEGER NOT NULL,

                quantity INTEGER NOT NULL CHECK(quantity > 0),

                FOREIGN KEY (sale_id)
                    REFERENCES sales(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (member_id)
                    REFERENCES members(id)
                    ON DELETE RESTRICT
            );
            """
        )

        conn.commit()
