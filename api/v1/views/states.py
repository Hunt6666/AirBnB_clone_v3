#!/usr/bin/python3
""" states api   """

from api.v1.views import app_views
from flask import request, jsonify
from flask import Flask
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ gets a list of all states"""
    lst = []
    objs = storage.all('State')
    for k, v in objs.items():
        lst += [v.to_dict()]
    return jsonify(lst)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_by_id(state_id):
    """ gets a single state by id """
    if request.method == 'GET':
        st = storage.get("State", state_id)
        if st is None:
            return jsonify({"error": "Not found"}), 404
        else:
            return jsonify(st.to_dict())
    if request.method == 'DELETE':
        st = storage.get("State", state_id)
        if st == None:
            return jsonify({"error": "Not found"}), 404
        else:
            key = "State." + str(state_id)
            storage.delete(st)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        st = storage.get("State", state_id)
        if st == None:
            return jsonify({"error": "Not found"}), 404
        else:
            return "not complete path not yet made"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
