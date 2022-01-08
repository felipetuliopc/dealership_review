# pylint: disable=missing-function-docstring,no-self-use

import os


def avoid_log_on_test(function):
    def wrapper(*args, **kwargs):
        if os.getenv('ENV') == 'test':
            return None
        return function(*args, **kwargs)
    return wrapper


class Logger:
    """
    Wrapper for a logger class
    """

    @avoid_log_on_test
    def debug(self, message):
        print(f'### DEBUG /// {message}')

    @avoid_log_on_test
    def info(self, message):
        print(f'### INFO /// {message}')

    @avoid_log_on_test
    def warning(self, message):
        print(f'### WARNING /// {message}')

    @avoid_log_on_test
    def error(self, message):
        print(f'### ERROR /// {message}')

    @avoid_log_on_test
    def critical(self, message):
        print(f'### CRITICAL /// {message}')
