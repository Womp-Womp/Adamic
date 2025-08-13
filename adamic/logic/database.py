import sqlite3
from pathlib import Path



class Database:
    """Simple SQLite-based storage for user experience points and ratings."""

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
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ratings (
                user_id TEXT,
                passage TEXT,
                rating INTEGER NOT NULL,
                PRIMARY KEY (user_id, passage)
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

    # Rating helpers
    def set_rating(self, user_id: str, passage: str, rating: int) -> float:
        """Store a user's rating for a passage and return new average rating."""
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO ratings (user_id, passage, rating) VALUES (?, ?, ?)
            ON CONFLICT(user_id, passage) DO UPDATE SET rating=excluded.rating
            """,
            (user_id, passage, rating),
        )
        self.conn.commit()
        return self.get_average_rating(passage)

    def get_average_rating(self, passage: str) -> float:
        cur = self.conn.cursor()
        cur.execute("SELECT AVG(rating) FROM ratings WHERE passage=?", (passage,))
        row = cur.fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0

    def close(self) -> None:
        self.conn.close()
