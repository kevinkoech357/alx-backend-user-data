#!/usr/bin/env python3

"""
Set up a basic Flask app.
"""

from flask import Flask, jsonify
from typing import List


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def return_json_message() -> dict:
    """
    Return a JSON payload.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
