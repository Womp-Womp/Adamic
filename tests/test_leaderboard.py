import time
from pathlib import Path

from adamic.logic.database import Database
from adamic.logic.leaderboard import top_users


def create_db(tmp_path: Path) -> Database:
    return Database(tmp_path / "xp.db")


def test_leaderboard_all_time(tmp_path):
    db = create_db(tmp_path)
    db.set_xp("alice", 30)
    db.set_xp("bob", 20)

    rows = top_users(db, page=1, period="all-time")
    assert rows[0][0] == "alice"
    assert rows[0][1] == 30
    assert rows[1][0] == "bob"


def test_leaderboard_weekly_filter(tmp_path):
    db = create_db(tmp_path)
    now = int(time.time())
    db.set_xp("alice", 40)
    db.add_event("alice", 40, timestamp=now - 2 * 86400)
    db.set_xp("bob", 50)
    db.add_event("bob", 50, timestamp=now - 10 * 86400)

    rows = top_users(db, page=1, period="weekly")
    assert rows[0][0] == "alice"
    assert rows[0][1] == 40
    assert all(r[0] != "bob" for r in rows)


def test_leaderboard_pagination(tmp_path):
    db = create_db(tmp_path)
    for i in range(1, 12):
        db.set_xp(f"user{i}", i)

    first_page = top_users(db, page=1, period="all-time", page_size=5)
    second_page = top_users(db, page=2, period="all-time", page_size=5)

    assert first_page[0][0] == "user11"
    assert second_page[0][0] == "user6"
