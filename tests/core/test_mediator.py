# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch

from dealership_review.core.mediator import Mediator


class TestMediator(unittest.TestCase):
    """
    Tests for the Mediator class
    """

    def setUp(self) -> None:
        self.mediator = Mediator()

    @patch(
        'dealership_review.core.dealership_review_scrapper.DealerShipReviewScrapper.scrap_reviews'
    )
    def test_get_scores(self, mocked_scrap_reviews):
        mocked_scrap_reviews.return_value = [
            {
                'reviewer': 'First Reviewer',
                'overall-score': 21,
                'employees-scores': [43],
                'message': 'First Message',
                'recommend-dealer': True,
                'specific-scores': {
                    'pricing': 56,
                },
            },
            {
                'reviewer': 'Second Reviewer',
                'overall-score': 98,
                'employees-scores': [76, 54],
                'message': 'Second Message',
                'recommend-dealer': False,
                'specific-scores': {
                    'customer-service': 32,
                },
            },
        ]

        scores = self.mediator.get_scores()
        reviewers_names = list(map(lambda review: review.reviewer, scores))

        self.assertEqual(reviewers_names, ['Second Reviewer', 'First Reviewer'])
