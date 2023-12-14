#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.authorized import Authorized
from models.user import User
from models import storage
from api.v1.views import app_views
from api.v1.views.validating import validate
from flask import abort, jsonify, make_response, request, session
from hashlib import md5
import validators


# User session data structure for authentication

@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ User login """

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Email not found")
    if 'password' not in data:
        abort(400, description="Password not found")

    all_users = storage.all(User).values()

    if not all_users:
        abort(404)

    valid = validate(data)
    if valid is not None:
        return make_response(jsonify({'message': valid}), 400)

    hash_password = md5(data['password'].encode()).hexdigest()

    for user in all_users:
        if user.email == data['email'] and\
                user.password == hash_password:
            Authorized.add(user)
            user_o = user.to_dict()
            return make_response(jsonify(user_o), 201)

    return (make_response(
        jsonify({'message': 'E-mail or password is incorrect'}), 401))


@app_views.route('/logout/<user_id>', methods=['DELETE'], strict_slashes=False)
def logout(user_id):
    """  User log out """
    user = storage.get(User, user_id)
    if Authorized.remove(user):
        return make_response(
                jsonify({'message': 'Successfully Logged out'}), 200)

    return make_response(
            jsonify({'message': 'No such user is logged in'}), 404)


@app_views.route('/me/<user_id>', methods=['GET'], strict_slashes=False)
def me(user_id):
    """ Get loged in User """
    user = storage.get(User, user_id)
    if Authorized.is_auth(user):
        return make_response(jsonify(user.to_dict()), 200)
    return (make_response(jsonify({'message': 'User Not Found'}), 404))


@app_views.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ User sign up """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    required_fields = [
        'email',
        'password',
        'first_name',
        'last_name']

    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    if 'email' in data and not validators.email(data['email']):
        abort(400, description="Invalid email format")

    existing_users = storage.all(User).values()
    for user in existing_users:
        if user.email == data['email']:
            abort(400, description="Email already exists")

    new_user = User(**data)
    new_user.save()
    # By default: a new user is automatically authorized
    Authorized.add(new_user)
    user_data = new_user.to_dict()

    return make_response(jsonify(user_data), 201)
