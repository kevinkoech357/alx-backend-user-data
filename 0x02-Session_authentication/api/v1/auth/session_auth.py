#!/usr/bin/env python3

"""
Define SessionAuth class that inherits from Auth.
"""


from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Inherit from Auth.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session id for user id
        """
        if user is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
