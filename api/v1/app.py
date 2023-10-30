#!/usr/bin/python3
"""module containing Flask web application API."""

from models import storage
from api.v1.views import app_views

import os
from flask import Flask, jsonify

from flask_cors import CORS


app = Flask(__name__)
""" initializes flask web application instance."""
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')

app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False

app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    """flask app request and event listener."""
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ controls 404 HTTP error."""
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """ 400 HTTP error message generator."""
    message = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        message = error.description
    return jsonify(error=message), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')

    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
