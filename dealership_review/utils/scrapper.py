from __future__ import annotations

from bs4 import BeautifulSoup, element as beautiful_soup_element

from dealership_review.exceptions.scrapper_exceptions import ElementNotFound


class ScrapperSearchable:
    """
    Implementation of a searchable object in the scrapper package
    """

    def __init__(self, base_element):
        self.base_element = base_element

    def find_first_element(self, name: str, cls: str = None, attrs: dict = None) -> ScrapperElement:
        """
        Finds the first element with the given conditions.
        If no element is found, ElementNotFound exception is raised.
        """
        element = self.base_element.find(name, class_=cls, attrs=attrs)

        if not element:
            raise ElementNotFound()

        return ScrapperElement(element)

    def find_all_elements(self, name: str, cls: str = None, attrs: dict = None) -> list:
        """
        Finds all element with the given conditions
        """

        def to_scrapper_element(element: beautiful_soup_element) -> ScrapperElement:
            return ScrapperElement(element)

        elements = self.base_element.find_all(name, class_=cls, attrs=attrs)

        return list(map(to_scrapper_element, elements))

    def count_elements(self, name: str, cls: str = None, attrs: dict = None) -> int:
        """
        Returns the quantity of elements found with the given conditions
        """
        elements = self.find_all_elements(name, cls, attrs)

        return len(elements)


class ScrapperElement(ScrapperSearchable):
    """
    Wrapper for a single element that the scrapper package may use
    """
    def __init__(self, element: beautiful_soup_element):
        self.element = element
        super().__init__(self.element)

    def get_value(self) -> str:
        return self.element.string


class Scrapper(ScrapperSearchable):
    """
    Wrapper for an HTML scrapper package
    """

    def __init__(self, html: str):
        self.html = html
        base_element = BeautifulSoup(html, 'html.parser')
        super().__init__(base_element)
