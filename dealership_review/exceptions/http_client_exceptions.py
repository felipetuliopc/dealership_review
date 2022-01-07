class FailedToDecodeFromJson(Exception):
    """
    Exception raised for errors in the json decode from the http client package
    """

    def __init__(self):
        self.message = 'It was not possible to decode json'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class HttpRequestDidNotReturnOk(Exception):
    """
    Exception raised for errors in the json decode from the http client package
    """

    def __init__(self):
        self.message = 'Response did not have status code 200'
        super().__init__(self.message)

    def __str__(self):
        return self.message
