"""Utilities for querying XP leaderboards."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Sequence

from .database import Database


PAGE_SIZE = 10


def top_users(
    db: Database,
    page: int = 1,
    period: str = "all-time",
    page_size: int = PAGE_SIZE,
) -> Sequence[tuple[str, int]]:
    """Return a slice of the leaderboard.

    Args:
        db: Database instance.
        page: 1-indexed page number.
        period: ``"all-time"`` or ``"weekly"``.
        page_size: Number of rows per page.

    Returns:
        A sequence of ``(user_id, points)`` tuples ordered by points desc.
    """

    offset = (page - 1) * page_size
    since: datetime | None = None
    if period.lower() == "weekly":
        since = datetime.utcnow() - timedelta(days=7)
    return db.leaderboard(limit=page_size, offset=offset, since=since)

