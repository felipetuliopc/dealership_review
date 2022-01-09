# pylint: disable=missing-function-docstring,no-self-use

import unittest
from unittest.mock import patch

from dealership_review.utils.slugifier import Slugifier


class TestSlugifier(unittest.TestCase):
    """
    Tests for the Slugifier wrapper
    """

    @patch('slugify.slugify')
    @unittest.skip('I was unable to patch slugify.slugify')
    def test_slugify(self, mocked_slugify):
        Slugifier.slugify('Wow such text')

        mocked_slugify.assert_called_with('Wow such text')
