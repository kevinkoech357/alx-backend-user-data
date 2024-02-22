#!/usr/bin/env python3

"""
Hash password using bcrypt.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Takes a password and returns bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate uuid and return its string representation.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Take email and password required arguments and return a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        Generate a session id based on user mail.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            # Handle case where user is not found
            raise ValueError

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Take a single session_id string argument
        and return the corresponding User or None.
        """
        if session_id is None:
            return None

        user = self._db.find_user_by(session_id=session_id)

        if user is None:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Take a single user_id integer argument and return None.
        """
        user = self._db.find_user_by(id=user_id)
        if user:
            user.session_id = None
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Finds the specified user based on email
        and generates a uuid str to be set
        as reset_token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            self._db._session.commit()
            return reset_token
        except NoResultFound:
            # Handle case where user is not found
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Takes a reset_token and a password then returns
        None.
        """
        if not isinstance(reset_token, str) or not isinstance(password, str):
            return {"error": "Wrong input format"}

        user = self._db.find_user_by(reset_token=reset_token)

        # Raise ValueError if token is not found
        if not user:
            raise ValueError

        # Hash password and update user table
        hashed_password = _hash_password(password)

        self._db.update_user(
            id=user.id, hashed_password=hashed_password, reset_token=None)
        self._db._session.commit()
