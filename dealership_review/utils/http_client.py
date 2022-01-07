import requests

from dealership_review.exceptions.http_client_exceptions import (
    FailedToDecodeFromJson, HttpRequestDidNotReturnOk
)


class HttpClient:
    """
    Wrapper for an HTTP client package
    """

    def get_json(self, url: str) -> dict:
        """
        Makes an HTTP GET request and return a dict of the json payload
        """
        response = requests.get(url)

        self._validate_response_status_code(response)

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as exception:
            raise FailedToDecodeFromJson() from exception

    def get_html(self, url: str) -> str:
        """
        Makes an HTTP GET request and return the html
        """
        response = requests.get(url)

        self._validate_response_status_code(response)

        return response.text

    @staticmethod
    def _validate_response_status_code(response: requests.Response):
        """
        Runs a validation on the response status code and raise exceptions if needed
        """
        if response.status_code != 200:
            raise HttpRequestDidNotReturnOk
