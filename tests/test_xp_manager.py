from adamic.logic.database import Database
from adamic.logic.xp_manager import XPManager


def test_award_verse_view(tmp_path):
    db = Database(tmp_path / "xp.db")
    manager = XPManager(db)
    user = "alice"
    assert manager.get_xp(user) == 0
    manager.award_verse_view(user)
    assert manager.get_xp(user) == 1
    manager.award_verse_view(user, points=2)
    assert manager.get_xp(user) == 3


def test_award_quiz_answer(tmp_path):
    db = Database(tmp_path / "xp.db")
    manager = XPManager(db)
    user = "bob"
    manager.award_quiz_answer(user, correct=True)
    assert manager.get_xp(user) == manager.QUIZ_CORRECT_POINTS
    manager.award_quiz_answer(user, correct=False)
    expected = manager.QUIZ_CORRECT_POINTS + manager.QUIZ_INCORRECT_POINTS
    assert manager.get_xp(user) == expected


def test_persistence(tmp_path):
    db_path = tmp_path / "xp.db"
    db = Database(db_path)
    manager = XPManager(db)
    user = "eve"
    manager.award_verse_view(user)
    db.close()

    db2 = Database(db_path)
    manager2 = XPManager(db2)
    assert manager2.get_xp(user) == 1


def test_rating_influences_xp(tmp_path):
    db = Database(tmp_path / "xp.db")
    manager = XPManager(db)
    passage = "Genesis 1:1"
    user1 = "alice"
    user2 = "bob"
    manager.award_verse_view(user1, passage)
    assert manager.get_xp(user1) == 1
    avg, xp = manager.submit_rating(user2, passage, 4)
    assert avg == 4
    assert xp == 4
    manager.award_verse_view(user1, passage)
    assert manager.get_xp(user1) == 6
