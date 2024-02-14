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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decode Base64 string and return decoded value as UTF8 string.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode("utf-8")
            return decoded_string
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extract user email and password from
        the decoded Base64 authorization header.
        """
        if decoded_base64_authorization_header is None:
            return None

        if not isinstance(decoded_base64_authorization_header, str):
            return None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password
