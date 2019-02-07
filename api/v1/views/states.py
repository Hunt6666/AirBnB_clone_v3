#!/usr/bin/python3
"""
State api
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from flask import Flask
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ gets a list of all states or makes one"""
    if request.method == 'GET':
        lst = []
        objs = storage.all('State')
        for k, v in objs.items():
            lst += [v.to_dict()]
        return jsonify(lst)
    if request.method == 'POST':
        stf = request.get_json(silent=True)
        if stf is None:
            return jsonify("Not a JSON"), 400
        name = stf["name"]
        if name is None:
            return jsonify("Missing name"), 400
        st = State()
        st.name = name
        st.save()
        return jsonify(st.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_by_id(state_id):
    """ gets a single state by id shows deletes or alters it"""
    if request.method == 'GET':
        st = storage.get("State", state_id)
        if st is None:
            abort(404)
        else:
            return jsonify(st.to_dict())
    if request.method == 'DELETE':
        st = storage.get("State", state_id)
        if st is None:
            return jsonify({"error": "Not found"}), 404
        else:
            key = "State." + str(state_id)
            storage.delete(st)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        st = storage.get("State", state_id)
        if st is None:
            return jsonify({"error": "Not found"}), 404
        else:
            stf = request.get_json(silent=True)
            if stf is None:
                return jsonify("Not a JSON"), 400
            for k, v in stf.items():
                if k != "id" and k != "created_at" and k != "updated_at":
                    setattr(st, k, v)
            st.save()
            return jsonify(st.to_dict()), 200
