# pylint: disable=missing-function-docstring,too-many-arguments

import math
import re

POSITIVE_WORDS = [
    'good',
    'helpful',
    'comfortable',
    'pleasant',
    'easy',
    'excellent',
    'friendly',
    'fast',
    'happy',
    'thank',
    'nice',
    'amazing',
    'love',
]
NEGATIVE_WORDS = [
    'bad',
    'hard',
    'disappointed',
    'mistake',
    'slow',
    'stupid',
    'deceitful',
    'sad',
    'pain',
    'waste',
    'furious',
    'horrible',
    'hate',
]


class Review:
    """
    Entity that represents a review. Stores the data scrapped
    from the website and calculates a score for it.
    """

    def __init__(
            self,
            reviewer: str,
            overall_score: int,
            employees_scores: list = None,
            message: str = None,
            recommend_dealer: bool = None,
            specific_scores: dict = None
    ):
        self._reviewer = reviewer
        self._overall_score = overall_score
        self._employees_scores = employees_scores
        self._message = message
        self._recommend_dealer = recommend_dealer
        self._specific_scores = specific_scores
        self._score = self.calculate_score()

    def __str__(self):
        return f'{self.reviewer} scored {self.score}'

    @property
    def reviewer(self) -> str:
        return self._reviewer

    @property
    def score(self) -> int:
        return self._score

    def calculate_score(self) -> int:
        score = \
            self._calculate_recommend_dealer_score() + \
            self._calculate_overall_score() + \
            self._calculate_score_from_message() + \
            self._calculate_employees_score() + \
            self._calculate_specific_scores()

        return max(score, 0)

    def _calculate_recommend_dealer_score(self) -> int:
        if self._recommend_dealer:
            return 40
        return 0

    def _calculate_overall_score(self) -> int:
        return math.floor(0.4 * self._overall_score)

    def _calculate_employees_score(self) -> int:
        employees_count = len(self._employees_scores)

        if employees_count == 0:
            return 0

        return math.floor(0.2 * sum(self._employees_scores) / employees_count)

    def _calculate_score_from_message(self) -> int:
        score = 0

        lowercase_message = self._message.lower()
        lowercase_message_without_punctuation = re.sub(r'[^\w\s]', '', lowercase_message)
        words = lowercase_message_without_punctuation.split()

        score += min(len(set(POSITIVE_WORDS) & set(words)), 10)
        score -= min(len(set(NEGATIVE_WORDS) & set(words)), 10)

        return score

    def _calculate_specific_scores(self) -> int:
        specific_scores_values = list(self._specific_scores.values())
        specific_scores_count = len(specific_scores_values)

        if specific_scores_count == 0:
            return 0

        return math.floor(0.4 * sum(specific_scores_values) / specific_scores_count)
