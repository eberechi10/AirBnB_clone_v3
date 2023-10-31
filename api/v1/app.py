#!/usr/bin/python3
""" Module that defines the app file """

from os import getenv
from flask import Flask, jsonify

from flask_cors import CORS
from api.v1.views import app_views

from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_flask(exception):
    """flask context to listener."""
    # print(exception)
    storage.close()


@app.errorhandler(404)
def handle_404(erro):
    """Controls the 404 HTTP error code."""
    return jsonify(error="Not found"), 404


@app.errorhandler(400)
def handle_400(erro):
    """controls the 400 HTTP error."""

    if erro.description:
        return jsonify(error=erro.description), 400

    return jsonify(error="Bad Request"), 400


if __name__ == "__main__":
    env_host = getenv("HBNB_API_HOST", "0.0.0.0")

    env_port = getenv("HBNB_API_PORT", "5000")
    app.run(host=env_host, port=env_port, threaded=True)
