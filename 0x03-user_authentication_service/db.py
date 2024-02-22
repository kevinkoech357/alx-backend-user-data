#!/usr/bin/env python3


"""
DB module
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User
import bcrypt


class DB:
    """DB class"""

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save user to the database.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """
        Find a user by arbitrary keyword arguments.

        Raises:

        NoResultFound: If no user is found matching the filter criteria
        InvalidRequestError: If wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound as e:
            raise NoResultFound from e
        except InvalidRequestError as e:
            raise InvalidRequestError from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Use find_user_by to locate the user to update
        then will update the user’s attributes as passed
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute '{key}'")
            setattr(user, key, value)

        self._session.commit()
