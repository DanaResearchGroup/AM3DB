"""
AM3DB's user module.
"""

import os
from enum import Enum
from typing import Optional

from arc.common import read_yaml_file, save_yaml_file

from am3db.common import DATABASE_PATH


class StatusEnum(str, Enum):
    """
    The supported user status.

    Statuses are:
        'student': Can approve or reject a 3D AM.
        'contributor': Can populate the database with new reactions.
        'developer': Can modify the structure of the database.
        'admin': Can approve a rejected reaction.
    """
    student = 'student'
    contributor = 'contributor'
    developer = 'developer'
    admin = 'admin'


class User(object):
    """
    An AM3DB User class.

    Args:
        name (str): The username.
        status (str, optional): The user's status.

    Attributes:
        name (str): The username.
        status (str): The user's status.
    """

    def __init__(self,
                 name: str,
                 status: str = 'student',
                 ):
        self.name = name
        self.status = StatusEnum(status.lower())
        self.users_path = os.path.join(DATABASE_PATH, 'users.yml')
        self.users = None

    def load(self):
        """
        Load the users and status from the database.
        """
        self.users = read_yaml_file(self.users_path) if os.path.isfile(self.users_path) else dict()

    def update(self):
        """
        Update the user and status in the .users attribute.
        """
        if self.users is None:
            self.load()
        self.users[self.name] = self.status.value

    def save(self):
        """
        Save the user and status in the database.
        """
        self.update()
        save_yaml_file(path=self.users_path, content=self.users)


def get_user_from_file(name: str) -> Optional[User]:
    """
    Get a User object instance from the database.

    Args:
        name (str): The username.

    Returns:
        Optional[User]: The corresponding User object instance
    """
    users_path = os.path.join(DATABASE_PATH, 'users.yml')
    users = read_yaml_file(users_path) if os.path.isfile(users_path) else None
    if users is None:
        print(f'Error: User {name} does not have edit privileges in the system.\n')
        return None
    if name in users.keys():
        return User(name=name, status=users[name])
