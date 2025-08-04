import json
from pathlib import Path

class Bible:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            return json.load(f)

    def get_verse(self, book: str, chapter: int, verse: int) -> str:
        try:
            return self.data[book][str(chapter)][str(verse)]
        except KeyError:
            return "Verse not found."

    def get_chapter(self, book: str, chapter: int) -> dict:
        try:
            return self.data[book][str(chapter)]
        except KeyError:
            return {"error": "Chapter not found."}

    def get_books(self) -> list:
        return list(self.data.keys())
