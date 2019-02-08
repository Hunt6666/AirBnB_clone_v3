#!/usr/bin/python3
"""
Creating a new view for Cities
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify, abort, request
from os import environ
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def show_cities(state_id):
    """
    Shows all states in file storage
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = state.cities
    return jsonify([c.to_dict() for c in cities])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def show_a_city(city_id):
    """
    Shows the city associated with city id provided
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_a_city(city_id):
    """
    Deletes a city by city_id; if found
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_a_city(city_id):
    """
    Updates a city
    """
    info = request.get_json(silent=True)
    if not info:
        return "Not a JSON", 400
    city = storage.get("City", city_id)
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    if city is None:
        abort(404)
    else:
        for k, v in info.items():
            if k not in ignore:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_a_city(state_id):
    """
    Creates a new city using state_id
    """
    info = ""
    info = request.get_json(silent=True)
    if info is None:
        return "Not a JSON", 400
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    name = info.get("name")
    if name is None:
        return "Missing name", 400
    city = City()
    city.name = name
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201
