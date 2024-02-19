#!/usr/bin/env python3

"""
Set up a basic Flask app.
"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def return_json_message() -> dict:
    """
    Return a JSON payload.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> dict:
    """
    Endpoint to register user.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify(
            {"status": "error", "message": "Email and password are required"}
        ), 400

    try:
        user = AUTH.register_user(email, password)
        if user is not None:
            return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
