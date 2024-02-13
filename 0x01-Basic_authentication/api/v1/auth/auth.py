#!/usr/bin/env python3

"""
Define class Auth and all methods required
for user authentication.
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """
    Define authentication class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if path or excluded_paths is None
        and False if path in excluded_paths.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Making the paths slash tolerant
        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            if excluded_path.endswith("/"):
                excluded_path = excluded_path[:-1]
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Returns None.
        """
        return None
