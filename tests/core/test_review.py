# pylint: disable=missing-function-docstring

import unittest

from dealership_review.core.review import Review


class TestReview(unittest.TestCase):
    """
    Tests for the entity class Review
    """

    def setUp(self) -> None:
        reviewer = 'Doge'
        overall_score = 40
        employees_scores = [50, 30]
        message = 'Amazing experience!! Wow such happy!!'
        recommend_dealer = True
        specific_scores = {
            'pricing': 50,
            'customer-service': 10
        }
        self.review = Review(
            reviewer=reviewer,
            overall_score=overall_score,
            employees_scores=employees_scores,
            message=message,
            recommend_dealer=recommend_dealer,
            specific_scores=specific_scores,
        )

    def test_reviewer(self):
        self.assertEqual(self.review.reviewer, 'Doge')

    def test_score(self):
        self.assertEqual(self.review.score, 78)

    def test_score_with_a_modifier_word(self):
        reviewer = 'Doge'
        overall_score = 40
        employees_scores = [50, 30]
        message = 'Amazing experience!! Wow such happy!! Not bad!!'
        recommend_dealer = True
        specific_scores = {
            'pricing': 50,
            'customer-service': 10
        }
        review = Review(
            reviewer=reviewer,
            overall_score=overall_score,
            employees_scores=employees_scores,
            message=message,
            recommend_dealer=recommend_dealer,
            specific_scores=specific_scores,
        )

        self.assertEqual(review.score, 79)

    def test_score_with_another_modifier_word(self):
        reviewer = 'Doge'
        overall_score = 40
        employees_scores = [50, 30]
        message = "Amazing experience!! Wow such happy!! Wasn't good!!"
        recommend_dealer = True
        specific_scores = {
            'pricing': 50,
            'customer-service': 10
        }
        review = Review(
            reviewer=reviewer,
            overall_score=overall_score,
            employees_scores=employees_scores,
            message=message,
            recommend_dealer=recommend_dealer,
            specific_scores=specific_scores,
        )

        self.assertEqual(review.score, 77)
