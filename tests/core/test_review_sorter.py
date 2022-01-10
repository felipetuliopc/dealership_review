# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import MagicMock

from dealership_review.core.review_sorter import sort_reviews, SortType


class TestSortReviews(unittest.TestCase):
    """
    Tests for the sort_review function
    """

    def setUp(self) -> None:
        self.highest_score_review = MagicMock(score=0)
        self.medium_score_review = MagicMock(score=5)
        self.lowest_score_review = MagicMock(score=10)
        self.reviews = [
            self.medium_score_review,
            self.lowest_score_review,
            self.highest_score_review,
        ]

    def test_sort_reviews_ascending(self):
        expected_result = [
            self.highest_score_review,
            self.medium_score_review,
            self.lowest_score_review,
        ]

        self.assertEqual(
            sort_reviews(self.reviews, sort_type=SortType.ASC),
            expected_result
        )

    def test_sort_reviews_descending(self):
        expected_result = [
            self.lowest_score_review,
            self.medium_score_review,
            self.highest_score_review,
        ]

        self.assertEqual(
            sort_reviews(self.reviews, sort_type=SortType.DESC),
            expected_result
        )
