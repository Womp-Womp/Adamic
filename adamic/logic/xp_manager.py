from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .database import Database


@dataclass
class XPManager:
    """Manage experience points for users."""

    db: Database

    VERSE_VIEW_POINTS: int = 1
    QUIZ_CORRECT_POINTS: int = 10
    QUIZ_INCORRECT_POINTS: int = 0
    BADGE_THRESHOLDS: dict[str, int] = None

    def __post_init__(self) -> None:
        if self.BADGE_THRESHOLDS is None:
            self.BADGE_THRESHOLDS = {"100 Verses": 100}

    def get_xp(self, user_id: str) -> int:
        """Return the total XP for ``user_id``."""
        return self.db.get_xp(user_id)

    def award_verse_view(self, user_id: str, points: int | None = None) -> int:
        """Award XP for viewing a verse.

        Args:
            user_id: Identifier for the user.
            points: Optional override for the number of points to award.

        Returns:
            The user's new total XP.
        """
        delta = points if points is not None else self.VERSE_VIEW_POINTS
        total = self.db.increment_xp(user_id, delta)
        verses_read = self.db.increment_verses_read(user_id, 1)
        for badge, threshold in self.BADGE_THRESHOLDS.items():
            if verses_read >= threshold:
                self.db.add_badge(user_id, badge)
        return total

    def award_quiz_answer(
        self,
        user_id: str,
        correct: bool,
        points_correct: int | None = None,
        points_incorrect: int | None = None,
    ) -> int:
        """Award XP for answering a quiz question.

        Args:
            user_id: Identifier for the user.
            correct: Whether the user's answer was correct.
            points_correct: Optional override for points when correct.
            points_incorrect: Optional override for points when incorrect.

        Returns:
            The user's new total XP after awarding points.
        """
        if correct:
            delta = (
                points_correct if points_correct is not None else self.QUIZ_CORRECT_POINTS
            )
        else:
            delta = (
                points_incorrect
                if points_incorrect is not None
                else self.QUIZ_INCORRECT_POINTS
            )
        return self.db.increment_xp(user_id, delta)

    def get_badges(self, user_id: str) -> List[str]:
        return self.db.get_badges(user_id)

    def get_verses_read(self, user_id: str) -> int:
        return self.db.get_verses_read(user_id)
