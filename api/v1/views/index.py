#!/usr/bin/python3
"""
Starts a flask app
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns JSON
    """
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def count():
    """
    Count number of each object]
    """
    stats = {}
    stats['amenities'] = storage.count('Amenity')
    stats['cities'] =storage.count('City')
    stats['places'] =storage.count('Place')
    stats['reviews'] =storage.count('Review')
    stats['states'] =storage.count('State')
    stats['users'] =storage.count('User')
    return jsonify(stats)
