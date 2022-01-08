class ElementNotFound(Exception):
    """
    Exception raised when the searched element is not found in the document
    """

    def __init__(self):
        self.message = 'Element was not found in the document'
        super().__init__(self.message)

    def __str__(self):
        return self.message
