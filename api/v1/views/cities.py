#!/usr/bin/python3
"""
Creating a new view for Cities
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify, abort, request
from os import environ


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def show_cities(state_id):
    """
    Shows all states in file storage
    """
    cities = []
    for city in storage.all('City').values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    if cities != []:
        return jsonify(cities)
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def show_a_city(city_id):
    """
    Shows the city associated with city id provided
    """
    for city in storage.all('City').values():
        if city.id == city_id:
            return jsonify(city.to_dict())
        else:
            return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_a_city(city_id):
    """
    Deletes a city by city_id; if found
    """
    for city in storage.all('City').values():
        if city.id == city_id:
            city.delete()
            storage.save()
            return jsonify({}), 200
        else:
            return jsonify({"error": "Not found"}), 404


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_a_city(city_id):
    """
    Updates a city
    """
    info = request.get_json()
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for city in storage.all('City').values():
        if city.id == city_id:
            for k, v in info.items():
                if k not in ignore:
                    setattr(city, k, v)
        else:
            abort(404)
    city.save()
    if not info:
        return (jsonify({"error": "Not a JSON"}), 400)
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


if __name__ == "__main__":
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_PORT'] = '5000'
    app.run(host=environ['HBNB_API_HOST'],
            port=environ['HBNB_API_PORT'],
            threaded=True)
