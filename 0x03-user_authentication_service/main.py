#!/usr/bin/env python3

"""
Contains functions that test if the routes
in app.py return expected responses.
"""


import requests as rq


BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the provided email and password.
    """
    response = rq.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the provided email and an incorrect password.
    """
    response = rq.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in with the provided email and password and return the session ID.
    """
    response = rq.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 200


def profile_unlogged() -> None:
    """
    Attempt to access the profile page without being logged in.
    """
    response = rq.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Access the profile page using the provided session ID.
    """
    response = rq.get(
        f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 403


def log_out(session_id: str) -> None:
    """
    Log out using the provided session ID.
    """
    response = rq.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 403


def reset_password_token(email: str) -> str:
    """
    Request a reset token for the provided email.
    """
    response = rq.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password associated with the
    provided email using the reset token.
    """
    response = rq.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email, "reset_token": reset_token,
            "new_password": new_password},
    )
    assert response.status_code == 400


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
