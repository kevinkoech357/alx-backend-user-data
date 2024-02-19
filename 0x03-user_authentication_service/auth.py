#!/usr/bin/env python3

"""
Hash password using bcrypt.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Takes a password and returns bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
