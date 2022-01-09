# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch, MagicMock

from dealership_review.exceptions.scrapper_exceptions import ElementNotFound
from dealership_review.utils.scrapper import Scrapper, ScrapperElement


class TestScrapper(unittest.TestCase):
    """
    Tests for the Scrapper wrapper
    """

    def setUp(self) -> None:
        self.scrapper = Scrapper('<html></html>')

    @patch('bs4.BeautifulSoup.find')
    def test_find_first_element(self, mocked_find):
        mocked_find.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.find_first_element('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(element.get_value(), 'Wow such element')
        mocked_find.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find')
    def test_find_first_element_matching_value(self, mocked_find):
        mocked_find.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.find_first_element(
            'a',
            cls='wowsuchclass',
            attrs={'id': '123'},
            value='Wow such element',
        )

        self.assertEqual(element.get_value(), 'Wow such element')
        mocked_find.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find')
    def test_find_first_element_not_found(self, mocked_find):
        mocked_find.return_value = None

        with self.assertRaises(ElementNotFound):
            self.scrapper.find_first_element('a', cls='wowsuchclass', attrs={'id': '123'})
        mocked_find.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find')
    def test_find_first_element_matching_value_not_found(self, mocked_find):
        mocked_find.return_value = MagicMock(string='Wow such element')

        with self.assertRaises(ElementNotFound):
            self.scrapper.find_first_element(
                'a',
                cls='wowsuchclass',
                attrs={'id': '123'},
                value='Wow',
            )
        mocked_find.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_all')
    def test_find_all_elements(self, mocked_find_all):
        mocked_find_all.return_value = [
            MagicMock(string='Element 1'),
            MagicMock(string='Element 2'),
            MagicMock(string='Element 3'),
        ]

        elements = self.scrapper.find_all_elements('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(elements[0].get_value(), 'Element 1')
        self.assertEqual(elements[1].get_value(), 'Element 2')
        self.assertEqual(elements[2].get_value(), 'Element 3')
        mocked_find_all.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_all')
    def test_find_all_elements_matching_value(self, mocked_find_all):
        mocked_find_all.return_value = [
            MagicMock(string='Element 1'),
            MagicMock(string='Element 2'),
            MagicMock(string='Element 3'),
        ]

        elements = self.scrapper.find_all_elements(
            'a',
            cls='wowsuchclass',
            attrs={'id': '123'},
            value='Element 1',
        )

        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].get_value(), 'Element 1')
        mocked_find_all.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.select')
    def test_select_css(self, mocked_select):
        mocked_select.return_value = [
            MagicMock(string='Element 1'),
            MagicMock(string='Element 2'),
            MagicMock(string='Element 3'),
        ]

        elements = self.scrapper.select_css('a.class.another-class')

        self.assertEqual(elements[0].get_value(), 'Element 1')
        self.assertEqual(elements[1].get_value(), 'Element 2')
        self.assertEqual(elements[2].get_value(), 'Element 3')
        mocked_select.assert_called_with('a.class.another-class')

    @patch('bs4.BeautifulSoup.find_next_sibling')
    def test_find_next_sibling(self, mocked_find_next_sibling):
        mocked_find_next_sibling.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.find_next_sibling('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(element.get_value(), 'Wow such element')
        mocked_find_next_sibling.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_next_sibling')
    def test_find_next_sibling_matching_value(self, mocked_find_next_sibling):
        mocked_find_next_sibling.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.find_next_sibling(
            'a',
            cls='wowsuchclass',
            attrs={'id': '123'},
            value='Wow such element',
        )

        self.assertEqual(element.get_value(), 'Wow such element')
        mocked_find_next_sibling.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_next_sibling')
    def test_find_next_sibling_not_found(self, mocked_find_next_sibling):
        mocked_find_next_sibling.return_value = None

        with self.assertRaises(ElementNotFound):
            self.scrapper.find_next_sibling('a', cls='wowsuchclass', attrs={'id': '123'})
        mocked_find_next_sibling.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_next_sibling')
    def test_find_next_sibling_matching_value_not_found(self, mocked_find_next_sibling):
        mocked_find_next_sibling.return_value = MagicMock(string='Wow such element')

        with self.assertRaises(ElementNotFound):
            self.scrapper.find_next_sibling(
                'a',
                cls='wowsuchclass',
                attrs={'id': '123'},
                value='Wow',
            )
        mocked_find_next_sibling.assert_called_with('a', class_='wowsuchclass', attrs={'id': '123'})

    @patch('bs4.BeautifulSoup.find_previous_sibling')
    def test_find_previous_sibling(self, mocked_find_previous_sibling):
        mocked_find_previous_sibling.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.find_previous_sibling('a', cls='wowsuchclass', attrs={'id': '123'})

        self.assertEqual(element.get_value(), 'Wow such element')
        mocked_find_previous_sibling.assert_called_with(
            'a',
            class_='wowsuchclass',
            attrs={'id': '123'},
        )

    @patch('bs4.BeautifulSoup.find_previous_sibling')
    def test_find_previous_sibling_matching_value(self, mocked_find_previous_sibling):
        mocked_find_previous_sibling.return_value = MagicMock(string='Wow such element')

        element = self.scrapper.find_previous_sibling(
            'a',
            cls='wowsuchclass',
            attrs={'id': '123'},
            value='Wow such element',
        )

        self.assertEqual(element.get_value(), 'Wow such element')
        mocked_find_previous_sibling.assert_called_with(
            'a',
            class_='wowsuchclass',
            attrs={'id': '123'},
        )

    @patch('bs4.BeautifulSoup.find_previous_sibling')
    def test_find_previous_sibling_not_found(self, mocked_find_previous_sibling):
        mocked_find_previous_sibling.return_value = None

        with self.assertRaises(ElementNotFound):
            self.scrapper.find_previous_sibling('a', cls='wowsuchclass', attrs={'id': '123'})
        mocked_find_previous_sibling.assert_called_with(
            'a',
            class_='wowsuchclass',
            attrs={'id': '123'},
        )

    @patch('bs4.BeautifulSoup.find_previous_sibling')
    def test_find_previous_sibling_matching_value_not_found(self, mocked_find_previous_sibling):
        mocked_find_previous_sibling.return_value = MagicMock(string='Wow such element')

        with self.assertRaises(ElementNotFound):
            self.scrapper.find_previous_sibling(
                'a',
                cls='wowsuchclass',
                attrs={'id': '123'},
                value='Wow',
            )
        mocked_find_previous_sibling.assert_called_with(
            'a',
            class_='wowsuchclass',
            attrs={'id': '123'},
        )

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


class TestScrapperElement(unittest.TestCase):
    """
    Tests for the Scrapper Element
    """

    def test_get_value(self):
        element = MagicMock(string='Wow such string')
        scrapper_element = ScrapperElement(element)

        self.assertEqual(scrapper_element.get_value(), 'Wow such string')

    def test_get_class(self):
        element = {'class': ['wow', 'such', 'class']}
        scrapper_element = ScrapperElement(element)

        self.assertEqual(scrapper_element.get_class(), ['wow', 'such', 'class'])
