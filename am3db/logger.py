"""
AM3DB logger module
"""

import datetime
import os
import time

from arc.common import get_git_branch, get_git_commit

from am3db.common import AM3DB_PATH, VERSION, dict_to_str, time_lapse


class Logger(object):
    """
    The T3 Logger class.

    Args:
        user (str): The username.
        project (str): A project name.

    Attributes:
        user (str): The username.
        project (str): A project name.
        log_file (str): The path to the log file.
    """

    def __init__(self,
                 user: str,
                 project: str,
                 ):
        self.user = user
        self.project = project
        self.t0 = datetime.datetime.now()
        t0_str = self.t0.strftime("%Y.%m.%d %H.%M.%S")
        logs_path = os.path.join(AM3DB_PATH, 'logs')
        if not os.path.isdir(logs_path):
            os.mkdir(logs_path)
        self.log_file = os.path.join(logs_path, f'{self.user} {t0_str}.log')
        self.log_header()

    def log(self,
            message: str,
            level: str = 'info',
            ):
        """
        Log a message.
    
        Args:
            message (str): The message to be logged.
            level (str, optional): The message level. Controls the prefix and suffix to be added to the message.
                                   Allowed values are: 'info' (default), 'warning', and 'error'.
        """
        if level not in ['info', 'debug', 'warning', 'error', 'always'] and level is not None:
            self.log(f'Got an illegal level argument "{level}"', level='error')
            level = 'info'
        prefix = {'debug': '', 'info': '', 'warning': '\nWARNING: ', 'error': '\n\n\nERROR: ', 'always': ''}
        suffix = {'debug': '', 'info': '', 'warning': '\n', 'error': '\n\n', 'always': ''}
        if isinstance(message, dict):
            message = dict_to_str(message)
        elif not isinstance(message, str):
            message = str(message)
        message = prefix[level] + message + suffix[level] if level is not None else message
        print(message)
        if level is not None:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')

    def debug(self, message: str):
        """
        Log a debug level message.
        """
        self.log(message=message, level='debug')

    def info(self, message: str):
        """
        Log an info level message.
        """
        self.log(message=message, level='info')

    def warning(self, message: str):
        """
        Log a warning level message.
        """
        self.log(message=message, level='warning')

    def error(self, message: str):
        """
        Log an error level message.
        """
        self.log(message=message, level='error')

    def log_header(self):
        """
        Output a header to the log.
        """
        self.log(f'AM3DB execution initiated on {time.asctime()}\n\n'
                 f'###############################################################\n'
                 f'#                                                             #\n'
                 f'#                            AM3DB                            #\n'
                 f'#                  3D Atom Mapping Database                   #\n'
                 f'#                                                             #\n'
                 f'#                       Version: {VERSION}{" " * (10 - len(VERSION))}                   #\n'
                 f'#                                                             #\n'
                 f'################################################################\n\n',
                 level='always')

        # Extract HEAD git commit from AM3DB
        head, date = get_git_commit(path=AM3DB_PATH)
        branch_name = get_git_branch(path=AM3DB_PATH)
        if head != '' and date != '':
            self.log(f'The current git HEAD for AM3DB is:\n'
                     f'    {head}\n    {date}',
                     level='always')
        if branch_name and branch_name != 'main':
            self.log(f'    (running on the {branch_name} branch)\n',
                     level='always')
        else:
            self.log('\n', level='always')
        self.log(f'Starting project: "{self.project}"', level='always')
