#!/usr/bin/python3
""" states api   """

from api.v1.views import app_views
from flask import request, jsonify
from flask import Flask
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ gets a list of all states"""
    if request.method == 'GET':
        lst = []
        objs = storage.all('Amenity')
        for k, v in objs.items():
            lst += [v.to_dict()]
        return jsonify(lst)
    if request.method == 'POST':
        return "Not Done"


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_by_id(amenity_id):
    """ gets a single state by id """
    if request.method == 'GET':
        am = storage.get("Amenity", amenity_id)
        if am is None:
            return jsonify({"error": "Not found"}), 404
        else:
            return jsonify(am.to_dict())
    if request.method == 'DELETE':
        am = storage.get("Amenity", amenity_id)
        if am == None:
            return jsonify({"error": "Not found"}), 404
        else:
            storage.delete(am)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        am = storage.get("Amenity", amenity_id)
        if am == None:
            return jsonify({"error": "Not found"}), 404
        else:
            return "Not Done"

if __name__ == "__main__":
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_PORT'] = '5000'
    app.run(host=environ['HBNB_API_HOST'], port=environ['HBNB_API_PORT'],
            threaded=True)
