# pylint: disable=missing-function-docstring

import os
import unittest

from bs4 import BeautifulSoup


class TestBeautifulSoupPackage(unittest.TestCase):
    """
    Tests to learn how to use the Beautiful Soup package
    """

    def setUp(self) -> None:
        path = os.path.join(os.path.dirname(__file__), '../resources/hello_world.html')
        self.file = open(path, 'r', encoding='utf8')  # pylint: disable=consider-using-with
        html = self.file.read()

        self.soup = BeautifulSoup(html, 'html.parser')

    def test_read_file(self):
        self.assertTrue(self.soup.prettify())

    def test_get_title(self):
        self.assertEqual(self.soup.title.string, 'Wow, such Title')

    def test_get_first_li(self):
        self.assertEqual(self.soup.li.string, 'First item')

    def test_get_li_count(self):
        self.assertEqual(len(self.soup.find_all('li')), 3)

    def test_get_paragraph_with_specific_class(self):
        self.assertEqual(self.soup.find('p', class_='wow-such-class').string, 'Lorem ipsum')

    def test_search_for_element_that_doesnt_exist(self):
        self.assertFalse(self.soup.marquee)

    def test_get_value_of_element_that_doesnt_exist(self):
        with self.assertRaises(AttributeError):
            _ = self.soup.marquee.string

    def test_get_child_from_parent(self):
        parent = self.soup.find('ul')
        children = parent.find_all('li')

        self.assertEqual(len(children), 3)

    def test_get_class_from_element(self):
        element = self.soup.find('p', class_='class-such-wow')

        self.assertEqual(element['class'], ['wow-such-another-class', 'class-such-wow'])

    def test_get_class_from_element_via_css(self):
        elements = self.soup.select('p.class-such-wow.wow-such-another-class')

        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]['class'], ['wow-such-another-class', 'class-such-wow'])

    def test_get_class_from_element_via_css_in_different_order(self):
        elements = self.soup.select('p.wow-such-another-class.class-such-wow')

        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]['class'], ['wow-such-another-class', 'class-such-wow'])

    def test_get_next_sibling_element(self):
        element = self.soup.find('p', class_='wow-such-class')
        next_sibling_element = element.find_next_sibling('p')

        self.assertEqual(next_sibling_element.text, 'dolor sit amet.')

    def test_get_previous_sibling_element(self):
        element = self.soup.find('p', class_='wow-such-another-class')
        next_sibling_element = element.find_previous_sibling('p')

        self.assertEqual(next_sibling_element.text, 'Lorem ipsum')

    def test_get_previous_sibling_element_from_first_born(self):
        element = self.soup.find('p', class_='wow-such-class')
        next_sibling_element = element.find_previous_sibling('p')

        self.assertEqual(next_sibling_element, None)

    def tearDown(self) -> None:
        self.file.close()
