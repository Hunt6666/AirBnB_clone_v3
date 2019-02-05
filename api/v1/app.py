#!/usr/bin/python3
"""
Starting an API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from werkzeug.exceptions import NotFound
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close(content):
    """
    handling teardowns
    """
    storage.close()

@app.errorhandler(NotFound)
def not_found(error):
    """
    Returns a 404 status code
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
