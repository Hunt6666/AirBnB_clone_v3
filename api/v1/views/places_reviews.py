#!/usr/bin/python3
""" reviews api   """

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from flask import Flask
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['POST', 'GET'],
                 strict_slashes=False)
def places_review(place_id):
    """ show all reviews for a place or makes new one"""
    if request.method == 'GET':
        place = storage.get('Place', place_id)
        if place is None:
            abort(404)
        objs = storage.all('Review')
        reviews = []
        for k, v in objs.items():
            if v.place_id == place_id:
                reviews += [v.to_dict()]
        return jsonify(reviews)
    if request.method == 'POST':
        place = storage.get('Place', place_id)
        if place is None:
            abort(404)
        stf = request.get_json(silent=True)
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
            txt = stf['text']
        except:
            return jsonify("Missing text"), 400
        rv = Review()
        rv.user_id = u_id
        rv.text = txt
        rv.place_id = place_id
        rv.save()
        return jsonify(rv.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_by_id(review_id):
    """ gets a single review by id shows deletes or alters it"""
    ignore = ['id', 'created_at', 'updated_at', 'user_id',
              'place_id', "user"]
    if request.method == 'GET':
        rv = storage.get("Review", review_id)
        if rv is None:
            return jsonify({"error": "Not found"}), 404
        else:
            return jsonify(rv.to_dict())
    if request.method == 'DELETE':
        rv = storage.get("Review", review_id)
        if rv is None:
            return jsonify({"error": "Not found"}), 404
        else:
            storage.delete(rv)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        rv = storage.get("Review", review_id)
        if rv is None:
            abort(404)
        else:
            stf = request.get_json()
            if stf is None:
                return jsonify("Not a JSON"), 400
            for k, v in stf.items():
                if k not in ignore:
                    setattr(rv, k, v)
            rv.save()
            r_id = rv.id
            storage.reload()
            rv = storage.get("Review", r_id)
            return jsonify(rv.to_dict()), 200
