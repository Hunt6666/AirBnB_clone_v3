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
    cities = []
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for city in storage.all('City').values():
        if city.state_id == state_id and state.id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)



@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def show_a_city(city_id):
    """
    Shows the city associated with city id provided
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict()), 200
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_a_city(city_id):
    """
    Deletes a city by city_id; if found
    """
    city = storage.get("City", city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_a_city(city_id):
    """
    Updates a city
    """
    info = request.get_json(silent=True)
    city = storage.get("City", city_id)
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    if not info:
        return "Not a JSON", 400
    if not city:
        abort(404)
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
    info = request.get_json()
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if not info.get('name'):
        return "Missing name", 400
    if not info:
        return "Not a JSON", 400
    info['state_id'] = state_id
    city = City(**info)
    city.save()
    return jsonify(city.to_dict()), 201
