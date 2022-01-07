# pylint: disable=missing-function-docstring

import logging
import os


def avoid_log_on_test(function):
    def wrapper(*args, **kwargs):
        if os.getenv('ENV') == 'test':
            return
        return function(*args, **kwargs)
    return wrapper


class Logger:
    """
    Wrapper for a logger class
    """

    def __init__(self):
        logging.basicConfig(format='### %(levelname)s /// %(message)s')

    @avoid_log_on_test
    def debug(self, message):
        logging.debug(message)

    @avoid_log_on_test
    def info(self, message):
        logging.info(message)

    @avoid_log_on_test
    def warning(self, message):
        logging.warning(message)

    @avoid_log_on_test
    def error(self, message):
        logging.error(message)

    @avoid_log_on_test
    def critical(self, message):
        logging.critical(message)
