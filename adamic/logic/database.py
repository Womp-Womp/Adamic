import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence


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

            CREATE TABLE IF NOT EXISTS xp_events (
                user_id TEXT NOT NULL,
                points INTEGER NOT NULL,
                timestamp INTEGER NOT NULL
            )
            """
        )
        cur.execute(
            """
           CREATE TABLE IF NOT EXISTS xp_events (
                user_id TEXT NOT NULL,
                points INTEGER NOT NULL,
                timestamp INTEGER NOT NULL
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
        self.add_event(user_id, delta)
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
    # XP event helpers
    def add_event(
        self, user_id: str, points: int, timestamp: Optional[int] = None
    ) -> None:
        ts = int(timestamp if timestamp is not None else time.time())
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO xp_events (user_id, points, timestamp) VALUES (?, ?, ?)",
            (user_id, points, ts),
        )
        self.conn.commit()

    def leaderboard(
        self,
        limit: int,
        offset: int = 0,
        since: Optional[datetime] = None,
    ) -> Sequence[tuple[str, int]]:
        cur = self.conn.cursor()
        if since is None:
            cur.execute(
                "SELECT user_id, points FROM xp ORDER BY points DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
        else:
            cur.execute(
                """
                SELECT user_id, SUM(points) as total
                FROM xp_events
                WHERE timestamp >= ?
                GROUP BY user_id
                ORDER BY total DESC
                LIMIT ? OFFSET ?
                """,
                (int(since.timestamp()), limit, offset),
            )
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()
