"""
AM3DB common module
"""

import datetime
import os

VERSION = '0.1.0'

AM3DB_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # absolute path to the T3 folder
DATABASE_PATH = os.path.join(AM3DB_PATH, 'database')


def dict_to_str(dictionary: dict,
                level: int = 0,
                ) -> str:
    """
    A helper function to log dictionaries in a pretty way.

    Args:
        dictionary (dict): A general python dictionary.
        level (int): A recursion level counter, sets the visual indentation.

    Returns:
        str: A text representation for the dictionary.
    """
    message = ''
    for key, value in dictionary.items():
        if isinstance(value, dict):
            message += ' ' * level * 2 + str(key) + ':\n' + dict_to_str(value, level + 1)
        else:
            message += ' ' * level * 2 + str(key) + ': ' + str(value) + '\n'
    return message


def time_lapse(t0: datetime.datetime) -> datetime.timedelta:
    """
    A helper function returning the elapsed time since t0.

    Args:
        t0 (datetime.datetime): The initial time the count starts from.

    Returns: datetime.timedelta
        The time difference between now and t0.
    """
    return datetime.datetime.now() - t0
