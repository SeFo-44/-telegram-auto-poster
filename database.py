import sqlite3
from config import DATABASE_NAME


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(
            DATABASE_NAME,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            interval_hours INTEGER DEFAULT 1,
            current_post INTEGER DEFAULT 0
        )
        """)

        self.cursor.execute("""
        INSERT OR IGNORE INTO settings
        (id, interval_hours, current_post)
        VALUES (1,1,0)
        """)

        self.conn.commit()

    # -----------------------
    # Posts
    # -----------------------

    def add_post(self, text):
        self.cursor.execute(
            "INSERT INTO posts(text) VALUES(?)",
            (text,)
        )

        self.conn.commit()

    def get_posts(self):
        self.cursor.execute(
            "SELECT id,text FROM posts ORDER BY id"
        )

        return self.cursor.fetchall()

    def delete_post(self, post_id):
        self.cursor.execute(
            "DELETE FROM posts WHERE id=?",
            (post_id,)
        )

        self.conn.commit()

    # -----------------------
    # Settings
    # -----------------------

    def get_interval(self):
        self.cursor.execute(
            "SELECT interval_hours FROM settings WHERE id=1"
        )

        return self.cursor.fetchone()[0]

    def set_interval(self, hours):
        self.cursor.execute(
            "UPDATE settings SET interval_hours=? WHERE id=1",
            (hours,)
        )

        self.conn.commit()

    def get_current_post(self):
        self.cursor.execute(
            "SELECT current_post FROM settings WHERE id=1"
        )

        return self.cursor.fetchone()[0]

    def set_current_post(self, value):
        self.cursor.execute(
            "UPDATE settings SET current_post=? WHERE id=1",
            (value,)
        )

        self.conn.commit()
