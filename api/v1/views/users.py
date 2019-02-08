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
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def show_a_user(user_id):
    """
    Lists a user by using the user id
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def del_a_user(user_id):
    """
    Deletes a user by user_id; if found
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_a_user(user_id):
    """
    Updates a user by user_id
    """
    info = request.get_json(silent=True)
    user = storage.get('User', user_id)
    ignore = ['id', 'email', 'created_at', 'updated_at']
    if user is None:
        abort(404)
    else:
        if info is None:
            return "Not a JSON", 400
            for k, v in info.items():
                if k not in ignore:
                    setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_a_user():
    """
    Creates a new user
    """
    info = request.get_json(silent=True)
    if not info:
        return 'Not a JSON', 400
    if not info.get('email'):
        return "Missing email", 400
    if not info.get('password'):
        return "Missing password", 400
    user = User(**info)
    user.save()
    return jsonify(user.to_dict()), 201
