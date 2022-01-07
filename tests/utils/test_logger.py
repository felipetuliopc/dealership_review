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

    @patch('logging.debug')
    def test_debug(self, mocked_debug):
        Logger().debug('debug')

        mocked_debug.assert_called_with('debug')

    @patch('logging.info')
    def test_info(self, mocked_info):
        Logger().info('info')

        mocked_info.assert_called_with('info')

    @patch('logging.warning')
    def test_warning(self, mocked_warning):
        Logger().warning('warning')

        mocked_warning.assert_called_with('warning')

    @patch('logging.error')
    def test_error(self, mocked_error):
        Logger().error('error')

        mocked_error.assert_called_with('error')

    @patch('logging.critical')
    def test_critical(self, mocked_critical):
        Logger().critical('critical')

        mocked_critical.assert_called_with('critical')

    def tearDown(self) -> None:
        os.environ['ENV'] = 'test'
