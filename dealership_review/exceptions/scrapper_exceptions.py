class ElementNotFound(Exception):
    """
    Exception raised when the searched element is not found in the document
    """

    def __init__(self, name: str = None, cls: str = None, value: str = None):
        self.message = f'Element was not found in the document: <{name} class={cls}>{value}<{name}>'
        super().__init__(self.message)

    def __str__(self):
        return self.message
