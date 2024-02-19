#!/usr/bin/env python3

"""
Hash password using bcrypt.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Takes a password and returns bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[User, None]:
        """
        Register user if email and password is provided.
        """
        try:
            # Check if a user with the provided email already exists
            user = self._db.find_user_by(email=email)
            if user is not None:
                # User with the same email already exists, raise an exception
                raise ValueError(f"User {email} already exists.")

            # User with the provided email does not exist
            # proceed with registration
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        except NoResultFound:
            # User with the provided email does not exist
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        except Exception as e:
            # Handle any other exceptions
            raise e
