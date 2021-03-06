#!/usr/bin/python3
""" amenity api   """

from api.v1.views import app_views
from flask import request, jsonify
from flask import Flask
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ gets a list of all amenities or makes one"""
    if request.method == 'GET':
        lst = []
        objs = storage.all('Amenity')
        for k, v in objs.items():
            lst += [v.to_dict()]
        return jsonify(lst)
    if request.method == 'POST':
        stf = request.get_json()
        if stf is None:
            return jsonify("Not a JSON"), 400
        try:
            name = stf["name"]
        except:
            return jsonify("Missing name"), 400
        am = Amenity()
        am.name = name
        am.save()
        return jsonify(am.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_by_id(amenity_id):
    """ gets a single amenity by id shows deletes or alters it"""
    if request.method == 'GET':
        am = storage.get("Amenity", amenity_id)
        if am is None:
            return jsonify({"error": "Not found"}), 404
        else:
            return jsonify(am.to_dict())
    if request.method == 'DELETE':
        am = storage.get("Amenity", amenity_id)
        if am is None:
            return jsonify({"error": "Not found"}), 404
        else:
            storage.delete(am)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        am = storage.get("Amenity", amenity_id)
        if am is None:
            return jsonify({"error": "Not found"}), 404
        else:
            stf = request.get_json()
            if stf is None:
                return jsonify("Not a JSON"), 400
            for k, v in stf.items():
                if k != "id" and k != "created_at" and k != "updated_at":
                    setattr(am, k, v)
            am.save()
            return jsonify(am.to_dict()), 200
