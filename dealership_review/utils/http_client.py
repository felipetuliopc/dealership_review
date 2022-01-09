# pylint: disable=too-few-public-methods

import requests

from dealership_review.utils.logger import Logger

from dealership_review.exceptions.http_client_exceptions import (
    HttpRequestConnectionError, HttpRequestDidNotReturnOk
)


class HttpClient:
    """
    Wrapper for an HTTP client package
    """

    def __init__(self):
        self.logger = Logger()

    def get_html(self, url: str) -> str:
        """
        Makes an HTTP GET request and return the html
        """
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as exception:
            raise HttpRequestConnectionError() from exception

        self._validate_response_status_code(response)

        return response.text

    def _validate_response_status_code(self, response: requests.Response):
        """
        Runs a validation on the response status code and raise exceptions if needed
        """
        if response.status_code != 200:
            self.logger.error(
                f'Request made to {response.request.url} returned {response.status_code}'
            )
            raise HttpRequestDidNotReturnOk
