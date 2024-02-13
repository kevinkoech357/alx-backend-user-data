#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# Load the appropriate authentication instance
# based on the environment variable AUTH_TYPE
auth_type = os.environ.get("AUTH_TYPE")

if auth_type:
    if auth_type == "auth":
        # Import Auth from api.v1.auth.auth
        from api.v1.auth.auth import Auth

        # Create an instance of Auth and assign it to the variable auth
        auth = Auth()


@app.before_request
def handle_auth():
    """
    Handles authentication and authorization before each request.

    If auth is None, do nothing.
    If request.path is not part of the excluded paths list,
    do nothing (using require_auth method from auth instance).
    If Authorization header is missing, raises 401 error.
    If current user is None, raises 403 error.
    """
    if auth is None:
        return

    excluded_paths = [
        "/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"]
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_access(error) -> dict:
    """
    Handles unauthorized access.
    """
    return jsonify({"error": "Unathorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> dict:
    """
    Handles forbidden return if user is
    not allowed.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
