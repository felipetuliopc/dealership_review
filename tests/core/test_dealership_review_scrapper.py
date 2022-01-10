# pylint: disable=missing-function-docstring,too-many-locals

import unittest
from unittest.mock import MagicMock, patch

from dealership_review.core.dealership_review_scrapper import DealerShipReviewScrapper

from dealership_review.exceptions.http_client_exceptions import (
    HttpRequestDidNotReturnOk, HttpRequestConnectionError,
)
from dealership_review.exceptions.scrapper_exceptions import ElementNotFound

PAGES = 5
URL = 'https://www.wow.such.url'


class TestDealerShipReviewScrapper(unittest.TestCase):
    """
    Tests for the DealerShipReviewScrapper class
    """

    def setUp(self) -> None:
        self.dealership_review_scrapper = DealerShipReviewScrapper()

    @patch('dealership_review.utils.http_client.HttpClient.get_html')
    @patch('dealership_review.utils.scrapper.Scrapper.find_all_elements')
    def test_scrap_reviews(self, mocked_find_all_elements, mocked_get_html):
        mocked_name_element = MagicMock()
        mocked_name_element.get_value.side_effect = ['by Wow such name']

        mocked_overall_score_element = MagicMock()
        mocked_overall_score_element.get_class.side_effect = [['rating-12']]

        mocked_employee_score_element = MagicMock()
        mocked_employee_score_element.get_class.side_effect = [['rating-34']]

        mocked_employees_table_element = MagicMock()
        mocked_employees_table_element.find_all_elements.side_effect = [[
            mocked_employee_score_element
        ]]

        mocked_recommend_dealer_score_element = MagicMock()
        mocked_recommend_dealer_score_element.get_value.side_effect = [' Yes ']

        mocked_recommend_dealer_name_element = MagicMock()
        mocked_recommend_dealer_name_element.get_value.side_effect = ['Recommend Dealer']
        mocked_recommend_dealer_name_element.find_next_sibling.side_effect = [
            mocked_recommend_dealer_score_element
        ]

        mocked_recommend_dealer_root_element = MagicMock()
        mocked_recommend_dealer_root_element.find_first_element.side_effect = [
            mocked_recommend_dealer_name_element
        ]

        mocked_pricing_score_element = MagicMock()
        mocked_pricing_score_element.get_class.side_effect = [['rating-56']]

        mocked_pricing_name_element = MagicMock()
        mocked_pricing_name_element.get_value.side_effect = ['Pricing']
        mocked_pricing_name_element.find_next_sibling.side_effect = [mocked_pricing_score_element]

        mocked_pricing_root_element = MagicMock()
        mocked_pricing_root_element.find_first_element.side_effect = [mocked_pricing_name_element]

        mocked_specific_score_table_element = MagicMock()
        mocked_specific_score_table_element.find_all_elements.side_effect = [[
            mocked_recommend_dealer_root_element,
            mocked_pricing_root_element,
        ]]

        mocked_html_scrapper = MagicMock()
        mocked_html_scrapper.find_first_element.side_effect = [
            mocked_name_element,
            mocked_employees_table_element,
            mocked_specific_score_table_element,
        ]
        mocked_html_scrapper.select_css.side_effect = [
            [mocked_overall_score_element]
        ]

        mocked_get_html.return_value = '<html></html>'
        mocked_find_all_elements.return_value = [
            mocked_html_scrapper,
        ]

        result = self.dealership_review_scrapper.scrap_reviews(PAGES, URL)

        self.assertEqual(len(result), 1)
        self.assertEqual(result, [{
            'reviewer': 'Wow such name',
            'overall-score': 12,
            'employees-scores': [34],
            'recommend-dealer': True,
            'specific-scores': {
                'pricing': 56,
            },
        }])

    @patch('dealership_review.utils.http_client.HttpClient.get_html')
    @patch('dealership_review.utils.logger.Logger.error')
    def test_scrap_reviews_with_invalid_request(self, mocked_log_error, mocked_get_html):
        mocked_get_html.side_effect = MagicMock(side_effect=HttpRequestDidNotReturnOk())

        result = self.dealership_review_scrapper.scrap_reviews(PAGES, URL)

        self.assertFalse(result)
        mocked_log_error.assert_called_with('It was not possible to fetch data from DealerRater')

    @patch('dealership_review.utils.http_client.HttpClient.get_html')
    @patch('dealership_review.utils.logger.Logger.error')
    def test_scrap_reviews_with_failing_request(self, mocked_log_error, mocked_get_html):
        mocked_get_html.side_effect = MagicMock(side_effect=HttpRequestConnectionError())

        result = self.dealership_review_scrapper.scrap_reviews(PAGES, URL)

        self.assertFalse(result)
        mocked_log_error.assert_called_with('It was not possible to fetch data from DealerRater')

    @patch('dealership_review.utils.http_client.HttpClient.get_html')
    @patch('dealership_review.utils.scrapper.Scrapper.find_all_elements')
    @patch('dealership_review.utils.logger.Logger.error')
    def test_scrap_reviews_unable_to_find_element(
            self,
            mocked_log_error,
            mocked_find_all_elements,
            mocked_get_html,
    ):
        mocked_get_html.return_value = '<html></html>'
        mocked_find_all_elements.side_effect = MagicMock(side_effect=ElementNotFound())

        result = self.dealership_review_scrapper.scrap_reviews(PAGES, URL)

        self.assertFalse(result)
        mocked_log_error.assert_called_with(
            'Element was not found in the document: <None class=None>None<None>'
        )

    @patch('dealership_review.utils.http_client.HttpClient.get_html')
    @patch('dealership_review.utils.scrapper.Scrapper.find_all_elements')
    @patch('dealership_review.utils.logger.Logger.error')
    def test_scrap_reviews_unable_to_find_overall_score(
            self,
            mocked_log_error,
            mocked_find_all_elements,
            mocked_get_html,
    ):
        mocked_name_element = MagicMock()
        mocked_name_element.get_value.side_effect = ['by Wow such name']

        mocked_html_scrapper = MagicMock()
        mocked_html_scrapper.find_first_element.side_effect = [
            mocked_name_element,
        ]
        mocked_html_scrapper.select_css.side_effect = [[]]

        mocked_get_html.return_value = '<html></html>'
        mocked_find_all_elements.return_value = [
            mocked_html_scrapper,
        ]

        result = self.dealership_review_scrapper.scrap_reviews(PAGES, URL)

        self.assertFalse(result)
        mocked_log_error.assert_called_with('Overall score was not found')

    @patch('dealership_review.utils.http_client.HttpClient.get_html')
    @patch('dealership_review.utils.scrapper.Scrapper.find_all_elements')
    @patch('dealership_review.utils.logger.Logger.error')
    def test_scrap_reviews_unable_to_process_rating(
            self,
            mocked_log_error,
            mocked_find_all_elements,
            mocked_get_html,
    ):
        mocked_name_element = MagicMock()
        mocked_name_element.get_value.side_effect = ['by Wow such name']

        mocked_overall_score_element = MagicMock()
        mocked_overall_score_element.get_class.side_effect = [['wow-such-clas']]

        mocked_html_scrapper = MagicMock()
        mocked_html_scrapper.select_css.side_effect = [
            [mocked_overall_score_element]
        ]

        mocked_get_html.return_value = '<html></html>'
        mocked_find_all_elements.return_value = [
            mocked_html_scrapper,
        ]

        result = self.dealership_review_scrapper.scrap_reviews(PAGES, URL)

        self.assertFalse(result)
        mocked_log_error.assert_called_with('Rating could not be processed')
