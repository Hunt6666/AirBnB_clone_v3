#!/usr/bin/python3
""" places api   """

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from flask import Flask
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['POST', 'GET'],
                 strict_slashes=False)
def places_city(city_id):
    """ all places in a city or make place in city"""
    if request.method == 'GET':
        city = storage.get('City', city_id)
        if city is None:
            abort(404)
        objs = storage.all('Place')
        places = []
        for k, v in objs.items():
            if v.city_id == city_id:
                places += [v.to_dict()]
        return jsonify(places)
    if request.method == 'POST':
        stf = request.get_json(silent=True)
        city = storage.get('City', city_id)
        if city is None:
            abort(404)
        if stf is None:
            return jsonify("Not a JSON"), 400
        try:
            u_id = stf["user_id"]
        except:
            return jsonify("Missing user_id"), 400
        usr = storage.get("User", u_id)
        if usr is None:
            abort(404)
        try:
            name = stf['name']
        except:
            return jsonify("Missing name"), 400
        pl = Place()
        pl.user_id = u_id
        pl.name = name
        pl.city_id = city_id
        pl.save()
        return jsonify(pl.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_by_id(place_id):
    """ gets a single place by id shows, deletes or alters it"""
    if request.method == 'GET':
        pl = storage.get("Place", place_id)
        if pl is None:
            abort(404)
        else:
            return jsonify(pl.to_dict())
    if request.method == 'DELETE':
        pl = storage.get("Place", place_id)
        if pl is None:
            return jsonify({"error": "Not found"}), 404
        else:
            storage.delete(pl)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        pl = storage.get("Place", place_id)
        if pl is None:
            abort(404)
        else:
            try:
                stf = request.get_json(silent=True)
                if stf is None:
                    return jsonify("Not a JSON"), 400
            except:
                return jsonify("Not a JSON"), 400
            ignore = ["user", "id", "user_id", "city_id", "created_at",
                      "updated_at"]
            for k, v in stf.items():
                if (k not in ignore):
                    setattr(pl, k, v)
            pl.save()
            p_id = pl.id
            storage.reload()
            pll = storage.get("Place", p_id)
            return jsonify(pll.to_dict()), 200
