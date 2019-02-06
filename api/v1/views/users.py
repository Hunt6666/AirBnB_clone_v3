#!/usr/bin/python3
"""
User API
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import jsonify, abort, request
from os import environ
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def list_users():
    """
    Lists all users
    """
    for user in storage.all('User').values():
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def list_a_user(user_id):
    """
    Lists a user by using the user id
    """
    for user in storage.all('User').values():
        if user.id == user_id:
            return jsonify(user.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def del_a_user(user_id):
    """
    Deletes a user by user_id; if found
    """
    for user in storage.all('User').values():
        if user.id == user_id:
            user.delete()
            storage.save()
            return jsonify({}), 200
        else:
            return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_a_user(user_id):
    """
    Updates a user by user_id
    """
    info = request.get_json()
    user = storage.get('User', user_id)
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in info.items():
        if k not in ignore:
            setattr(user, k, v)
    if user is None:
        abort(404)
    if info is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_a_user():
    """
    Creates a new user
    """
    info = request.get_json()
    if info is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if not info.get('email'):
        return "Missing email", 400
    if not info.get('password'):
        return "Missing password", 400
    user = User(**info)
    user.save()
    return jsonify(user.to_dict()), 201


if __name__ == "__main__":
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_PORT'] = '5000'
    app.run(host=environ['HBNB_API_HOST'],
            port=environ['HBNB_API_PORT'],
            threaded=True)
