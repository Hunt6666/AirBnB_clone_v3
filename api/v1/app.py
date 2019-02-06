#!/usr/bin/python3
"""
Starting an API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from os import environ
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.teardown_appcontext
def close(Exception):
    """
    handling teardowns
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Returns a 404 status code
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    if not environ.get('HBNB_API_HOST'):
        host = environ['HBNB_API_HOST']
    if not environ.get('HBNB_API_PORT'):
        port = int(environ['HBNB_API_PORT'])
    app.run(host=host, port=port, threaded=True)
