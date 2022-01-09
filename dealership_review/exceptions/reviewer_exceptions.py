class OverallScoreNotFound(Exception):
    """
    Exception raised when the overall score is not found
    """

    def __init__(self):
        self.message = 'Overall score was not found'
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UnableToProcessRating(Exception):
    """
    Exception raised when the rating could not be processed
    """

    def __init__(self):
        self.message = 'Rating could not be processed'
        super().__init__(self.message)

    def __str__(self):
        return self.message
