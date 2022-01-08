from bs4 import BeautifulSoup, element as beautiful_soup_element

from dealership_review.exceptions.scrapper_exceptions import ElementNotFound


class Scrapper:
    """
    Wrapper for an HTML scrapper package
    """

    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_first_element(self, name: str, cls: str = None, attrs: dict = None) -> str:
        """
        Finds the first element with the given conditions.
        If no element is found, ElementNotFound exception is raised.
        """
        element = self.soup.find(name, class_=cls, attrs=attrs)

        if not element:
            raise ElementNotFound()

        return element.string

    def get_all_elements(self, name: str, cls: str = None, attrs: dict = None) -> list:
        """
        Finds all element with the given conditions
        """

        def to_string(element: beautiful_soup_element) -> str:
            return element.string

        elements = self.soup.find_all(name, class_=cls, attrs=attrs)

        return list(map(to_string, elements))

    def count_elements(self, name: str, cls: str = None, attrs: dict = None) -> int:
        """
        Returns the quantity of elements found with the given conditions
        """
        elements = self.get_all_elements(name, cls, attrs)

        return len(elements)
