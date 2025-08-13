from __future__ import annotations

from dataclasses import dataclass

from .database import Database


@dataclass
class XPManager:
    """Manage experience points for users."""

    db: Database

    VERSE_VIEW_POINTS: int = 1
    QUIZ_CORRECT_POINTS: int = 10
    QUIZ_INCORRECT_POINTS: int = 0

    def get_xp(self, user_id: str) -> int:
        """Return the total XP for ``user_id``."""
        return self.db.get_xp(user_id)

    def award_verse_view(
        self, user_id: str, passage: str | None = None, points: int | None = None
    ) -> int:
        """Award XP for viewing a verse.

        Args:
            user_id: Identifier for the user.
            passage: Optional passage identifier (e.g. "John 3:16").
            points: Optional override for the number of points to award.

        Returns:
            The user's new total XP.
        """
        delta = points if points is not None else self.VERSE_VIEW_POINTS
        if passage is not None:
            delta += round(self.db.get_average_rating(passage))
        return self.db.increment_xp(user_id, delta)

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

    def submit_rating(self, user_id: str, passage: str, rating: int) -> tuple[float, int]:
        """Record a user's rating and award XP based on the aggregate rating.

        Args:
            user_id: Identifier for the user.
            passage: Passage identifier (e.g. "John 3:16").
            rating: Rating value provided by the user.

        Returns:
            A tuple of (average rating for the passage, user's new total XP).
        """
        avg = self.db.set_rating(user_id, passage, rating)
        xp = self.db.increment_xp(user_id, round(avg))
        return avg, xp
