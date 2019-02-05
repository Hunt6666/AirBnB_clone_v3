#!/usr/bin/python3
"""
Starts a flask app
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns JSON
    """
    return jsonify({'status': 'OK'})
