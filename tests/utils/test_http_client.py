# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch, MagicMock

import requests

from dealership_review.exceptions.http_client_exceptions import (
    HttpRequestConnectionError, HttpRequestDidNotReturnOk
)
from dealership_review.utils.http_client import HttpClient


class TestHttpClient(unittest.TestCase):
    """
    Tests for the HttpClient wrapper
    """

    def setUp(self) -> None:
        self.http_client = HttpClient()

    @patch('requests.get')
    def test_get_html(self, mocked_get):
        html = '<!DOCTYPE html><html lang="en"></html>'
        mocked_get.return_value = MagicMock(
            status_code=200,
            text=html
        )

        response = self.http_client.get_html('http://www.wow.such.url')

        self.assertEqual(response, html)

    @patch('requests.get')
    def test_get_html_with_failing_request(self, mocked_get):
        mocked_get.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(HttpRequestConnectionError):
            self.http_client.get_html('http://www.wow.such.url')

    @patch('requests.get')
    def test_get_html_with_invalid_status_code(self, mocked_get):
        mocked_get.return_value = MagicMock(
            status_code=500,
        )

        with self.assertRaises(HttpRequestDidNotReturnOk):
            self.http_client.get_html('http://www.wow.such.url')
