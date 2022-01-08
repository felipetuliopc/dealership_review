# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch, MagicMock

from dealership_review.exceptions.scrapper_exceptions import ElementNotFound
from dealership_review.utils.scrapper import Scrapper


class TestScrapper(unittest.TestCase):
    """
    Tests for the Scrapper wrapper
    """

    def setUp(self) -> None:
        self.scrapper = Scrapper('<html></html>')

    @patch('bs4.BeautifulSoup.find')
    def test_get_first_element(self, mocked_find):
        mocked_find.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.get_first_element('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(element, 'Wow such element')
        mocked_find.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find')
    def test_get_first_element_not_found(self, mocked_find):
        mocked_find.return_value = None

        with self.assertRaises(ElementNotFound):
            self.scrapper.get_first_element('a', cls='wowsuchclass', attrs={'id': '123'})
        mocked_find.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_all')
    def test_get_all_elements(self, mocked_find_all):
        mocked_find_all.return_value = [
            MagicMock(string='Element 1'),
            MagicMock(string='Element 2'),
            MagicMock(string='Element 3'),
        ]

        elements = self.scrapper.get_all_elements('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(elements[0], 'Element 1')
        self.assertEqual(elements[1], 'Element 2')
        self.assertEqual(elements[2], 'Element 3')
        mocked_find_all.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_all')
    def test_count_elements(self, mocked_find_all):
        mocked_find_all.return_value = [
            MagicMock(string='Element 1'),
            MagicMock(string='Element 2'),
            MagicMock(string='Element 3'),
        ]

        count = self.scrapper.count_elements('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(count, 3)
        mocked_find_all.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})
