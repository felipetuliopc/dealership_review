# pylint: disable=missing-function-docstring,no-self-use

import unittest
from unittest.mock import patch

import os

from dealership_review.utils.logger import Logger


class TestLogger(unittest.TestCase):
    """
    Tests for the Logger wrapper
    """

    def setUp(self) -> None:
        os.environ['ENV'] = 'test_logger'

    @patch('builtins.print')
    def test_debug(self, mocked_print):
        Logger().debug('debug')

        mocked_print.assert_called_with('### DEBUG /// debug')

    @patch('builtins.print')
    def test_info(self, mocked_print):
        Logger().info('info')

        mocked_print.assert_called_with('### INFO /// info')

    @patch('builtins.print')
    def test_warning(self, mocked_print):
        Logger().warning('warning')

        mocked_print.assert_called_with('### WARNING /// warning')

    @patch('builtins.print')
    def test_error(self, mocked_print):
        Logger().error('error')

        mocked_print.assert_called_with('### ERROR /// error')

    @patch('builtins.print')
    def test_critical(self, mocked_print):
        Logger().critical('critical')

        mocked_print.assert_called_with('### CRITICAL /// critical')

    def tearDown(self) -> None:
        os.environ['ENV'] = 'test'
