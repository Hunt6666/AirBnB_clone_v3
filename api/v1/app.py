#!/usr/bin/python3
"""
Starting an API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from werkzeug.exceptions import NotFound
from flask import jsonify
from os import environ


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
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_PORT'] = '5000'
    app.run(host=environ['HBNB_API_HOST'], 
            port=environ['HBNB_API_PORT'], 
            threaded=True)
