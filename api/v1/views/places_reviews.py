#!/usr/bin/python3
""" reviews api   """

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from flask import Flask
from models import storage
from models.place import Place


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def reviews():
    """ gets a list of all reviews"""
    if request.method == 'GET':
        lst = []
        objs = storage.all('Review')
        for k, v in objs.items():
            lst += [v.to_dict()]
        return jsonify(lst)


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
        stf = request.get_json()
        place = storage.get('Place', place_id)
        if place is None:
            abort(404)
        if stf is None:
            return jsonify("Not a JSON"), 400
        u_id = stf["user_id"]
        if u_id is None:
            return jsonify("Missing user_id"), 400
        usr = storage.get("User", u_id)
        if usr is None:
            abort(404)
        txt = stf['text']
        if txt is None:
            return jsonify("Missing text"), 400
        rv = Review()
        rv.user_id = u_id
        rv.text = txt
        rv.save()
        return jsonify(rv.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_by_id(review_id):
    """ gets a single review by id shows deletes or alters it"""
    ignore = ['id', 'created_at', 'updated_at', 'user_id',
              'place_id']
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
            return jsonify(rv.to_dict()), 200


if __name__ == "__main__":
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_PORT'] = '5000'
    app.run(host=environ['HBNB_API_HOST'], port=environ['HBNB_API_PORT'],
            threaded=True)
