import pytest
from pathlib import Path
from adamic.bible import Bible

@pytest.fixture
def bible():
    data_path = Path(__file__).parent.parent / "adamic" / "data" / "sample_bible.json"
    return Bible(data_path)

def test_load_data(bible):
    assert bible.data is not None
    assert "Genesis" in bible.data
    assert "John" in bible.data

def test_get_verse(bible):
    verse = bible.get_verse("Genesis", 1, 1)
    assert verse == "In the beginning God created the heaven and the earth."

def test_get_verse_not_found(bible):
    verse = bible.get_verse("Genesis", 99, 99)
    assert verse == "Verse not found."

def test_get_chapter(bible):
    chapter = bible.get_chapter("John", 1)
    assert "1" in chapter
    assert "2" in chapter
    assert "3" in chapter

def test_get_books(bible):
    books = bible.get_books()
    assert "Genesis" in books
    assert "John" in books
