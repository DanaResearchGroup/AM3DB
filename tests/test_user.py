#!/usr/bin/env python3
# encoding: utf-8

"""
AM3DB user tests module
"""

import os
import shutil

from arc.common import read_yaml_file, save_yaml_file

from am3db import user
from am3db.common import DATABASE_PATH


def setup_module():
    """
    Setup.
    """
    users_path = os.path.join(DATABASE_PATH, 'users.yml')
    users_back_path = os.path.join(DATABASE_PATH, 'users_back.yml')
    if os.path.isfile(users_path):
        shutil.copy(src=users_path, dst=users_back_path)


def test_creating_and_saving_user():
    """Test creating and saving a user."""
    users_path = os.path.join(DATABASE_PATH, 'users.yml')
    assert not os.path.isfile(users_path)
    user_1 = user.User(name='IM')
    user_1.save()
    assert os.path.isfile(users_path)
    content = read_yaml_file(users_path)
    assert content == {'IM': 'student'}


def test_get_user_from_file():
    """Test the get_user_from_file() function."""
    users_path = os.path.join(DATABASE_PATH, 'users.yml')
    content = {'A': 'student',
               'B': 'admin',
               }
    save_yaml_file(path=users_path, content=content)
    user_1 = user.get_user_from_file('X')
    assert user_1 is None
    user_2 = user.get_user_from_file('A')
    assert isinstance(user_2, user.User)
    assert user_2.status.value == 'student'
    user_3 = user.get_user_from_file('B')
    assert user_3.status.value == 'admin'


def teardown_module():
    """
    Teardown any state that was previously setup with a setup_module method.
    """
    users_path = os.path.join(DATABASE_PATH, 'users.yml')
    users_back_path = os.path.join(DATABASE_PATH, 'users_back.yml')
    if os.path.isfile(users_path):
        os.remove(users_path)
    if os.path.isfile(users_back_path):
        shutil.copy(src=users_back_path, dst=users_path)
        os.remove(users_back_path)
