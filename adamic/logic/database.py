import sqlite3
from pathlib import Path
from typing import Optional


class Database:
    """Simple SQLite-based storage for user experience points."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS xp (
                user_id TEXT PRIMARY KEY,
                points INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    # Database interaction helpers
    def get_xp(self, user_id: str) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT points FROM xp WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        return int(row[0]) if row else 0

    def set_xp(self, user_id: str, points: int) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO xp (user_id, points) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET points=excluded.points
            """,
            (user_id, points),
        )
        self.conn.commit()

    def increment_xp(self, user_id: str, delta: int) -> int:
        current = self.get_xp(user_id)
        new_total = current + delta
        self.set_xp(user_id, new_total)
        return new_total

    def close(self) -> None:
        self.conn.close()
