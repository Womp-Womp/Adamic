import pytest
from pathlib import Path
from adamic.bible import Bible

@pytest.fixture
def bible():
    data_path = Path(__file__).parent.parent / "adamic" / "data" / "sample_bible.json"
    return Bible(data_path)

def test_search(bible):
    results = bible.search("beginning")
    assert "Genesis 1:1" in results
    assert "John 1:1" in results
    assert "John 1:2" in results
    assert len(results) == 3

def test_search_case_insensitive(bible):
    results = bible.search("BEGINNING")
    assert "Genesis 1:1" in results
    assert "John 1:1" in results
    assert "John 1:2" in results
    assert len(results) == 3

def test_search_no_results(bible):
    results = bible.search("nonexistent")
    assert len(results) == 0
