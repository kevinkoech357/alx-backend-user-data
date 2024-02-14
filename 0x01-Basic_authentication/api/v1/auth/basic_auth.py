#!/usr/bin/env python3

"""
Define BasicAuth class that inherits from Auth.
"""


from .auth import Auth
import base64


class BasicAuth(Auth):
    """
    Inherit from Auth.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Return Base64 part of the Authorization header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Extracting the Base64 part after 'Basic '
        base64_token = authorization_header.split(" ")[1]

        return base64_token
