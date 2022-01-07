# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch, MagicMock

import requests

from dealership_review.exceptions.http_client_exceptions import (
    FailedToDecodeFromJson, HttpRequestDidNotReturnOk
)
from dealership_review.utils.http_client import HttpClient


class TestHttpClient(unittest.TestCase):
    """
    Tests for the HttpClient wrapper
    """

    def setUp(self) -> None:
        self.http_client = HttpClient()

    @patch('requests.get')
    def test_get_json(self, mocked_get):
        json = {'wow': 'such', 'string': 123}
        mocked_get.return_value = MagicMock(
            status_code=200,
            json=lambda: json
        )

        response = self.http_client.get_json('http://www.wow.such.url')

        self.assertEqual(response, json)

    @patch('requests.get')
    def test_get_json_unable_to_decode_json(self, mocked_get):
        mocked_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(side_effect=requests.exceptions.JSONDecodeError())
        )

        with self.assertRaises(FailedToDecodeFromJson):
            self.http_client.get_json('http://www.wow.such.url')

    @patch('requests.get')
    def test_get_json_with_failing_request(self, mocked_get):
        mocked_get.return_value = MagicMock(
            status_code=500,
        )

        with self.assertRaises(HttpRequestDidNotReturnOk):
            self.http_client.get_json('http://www.wow.such.url')

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
        mocked_get.return_value = MagicMock(
            status_code=500,
        )

        with self.assertRaises(HttpRequestDidNotReturnOk):
            self.http_client.get_html('http://www.wow.such.url')
