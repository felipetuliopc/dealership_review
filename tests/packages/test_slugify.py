# pylint: disable=missing-function-docstring

import unittest

from slugify import slugify


class TestSlugifyPackage(unittest.TestCase):
    """
    Tests to learn how to use the Slugify package
    """

    def test_slugify(self):
        text = 'Wow such text'

        self.assertEqual(slugify(text), 'wow-such-text')
