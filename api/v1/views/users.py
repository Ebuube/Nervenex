#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from api.v1.views.validating import validate
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())

    return (jsonify(list_users))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)

    if not user:
        abort(404, description="User object not found")

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404, description="User object not found")

    storage.delete(user)
    storage.save()

    return make_response(jsonify({'message': 'User deleted successfully'}),
                         200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user():
    """
    Creates a user
    """
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    if 'first_name' not in data:
        abort(400, description="Missing first name")
    if 'last_name' not in data:
        abort(400, description="Missing last name")

    valid = validate(data)
    if valid is not None:
        return make_response(jsonify({'message': valid}), 400)

    instance = User(**data)
    instance.save()
    user = instance.to_dict()

    return make_response(jsonify(user), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404, description="User object not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    valid = validate(data)
    if valid is not None:
        return make_response(jsonify({'message': valid}), 400)

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    user = user.to_dict()

    return make_response(jsonify(user), 200)
