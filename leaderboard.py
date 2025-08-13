"""Simple script to query top users by XP."""

from __future__ import annotations

from pathlib import Path

from adamic.logic.database import Database
from adamic.logic.leaderboard import PAGE_SIZE, top_users


def main(period: str = "all-time", page: int = 1) -> None:
    db_path = Path(__file__).parent / "xp.db"
    db = Database(db_path)
    rows = top_users(db, page=page, period=period)
    base_rank = 1 + (page - 1) * PAGE_SIZE
    for idx, (user_id, points) in enumerate(rows, start=base_rank):
        print(f"{idx}. {user_id}: {points}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query XP leaderboard")
    parser.add_argument("period", choices=["all-time", "weekly"], nargs="?", default="all-time")
    parser.add_argument("page", type=int, nargs="?", default=1)
    args = parser.parse_args()
    main(args.period, args.page)

