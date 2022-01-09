# pylint: disable=missing-function-docstring,too-few-public-methods

from slugify import slugify as slg


class Slugifier:
    """
    Wrapper for a slugifier package
    """

    @staticmethod
    def slugify(text: str) -> str:
        return slg(text)
