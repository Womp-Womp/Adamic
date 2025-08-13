import json
import sqlite3
from pathlib import Path
from typing import List


class Database:
    """Simple SQLite-based storage for user profiles and experience points."""

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
            """,
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS profile (
                user_id TEXT PRIMARY KEY,
                verses_read INTEGER NOT NULL,
                badges TEXT NOT NULL
            )
            """,
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

    # Profile helpers
    def _ensure_profile(self, user_id: str) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO profile (user_id, verses_read, badges)
            VALUES (?, 0, ?)
            """,
            (user_id, json.dumps([])),
        )
        self.conn.commit()

    def get_verses_read(self, user_id: str) -> int:
        self._ensure_profile(user_id)
        cur = self.conn.cursor()
        cur.execute("SELECT verses_read FROM profile WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        return int(row[0]) if row else 0

    def increment_verses_read(self, user_id: str, delta: int) -> int:
        current = self.get_verses_read(user_id)
        new_total = current + delta
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE profile SET verses_read=? WHERE user_id=?",
            (new_total, user_id),
        )
        self.conn.commit()
        return new_total

    def get_badges(self, user_id: str) -> List[str]:
        self._ensure_profile(user_id)
        cur = self.conn.cursor()
        cur.execute("SELECT badges FROM profile WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        if not row:
            return []
        badges = json.loads(row[0])
        return list(badges)

    def add_badge(self, user_id: str, badge: str) -> List[str]:
        badges = self.get_badges(user_id)
        if badge not in badges:
            badges.append(badge)
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE profile SET badges=? WHERE user_id=?",
                (json.dumps(badges), user_id),
            )
            self.conn.commit()
        return badges

    def close(self) -> None:
        self.conn.close()
