# pylint: disable=missing-function-docstring

import unittest

import requests


class TestRequestsPackage(unittest.TestCase):
    """
    Tests to learn how to use the Requests package
    """

    def setUp(self) -> None:
        self.protocol_and_domain = 'https://httpbin.org'

    def test_make_get_request_with_json_response(self):
        response = requests.get(f'{self.protocol_and_domain}/get')

        self.assertTrue(response)
        self.assertTrue('args' in response.json())
        self.assertTrue('headers' in response.json())
        self.assertTrue('origin' in response.json())
        self.assertTrue('url' in response.json())

    def test_make_get_request_with_html_response(self):
        response = requests.get(f'{self.protocol_and_domain}/html')

        self.assertTrue(response)
        self.assertTrue(response.text.startswith('<!DOCTYPE html>'))
