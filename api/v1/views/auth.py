#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from api.v1.views.validating import validate
from flask import abort, jsonify, make_response, request, session
from hashlib import md5
import validators


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
            user_o = user.to_dict()
            session['user'] = user_o
            return (jsonify(user_o))

    return (make_response(
        jsonify({'message': 'E-mail or password is incorrect'}), 400))


@app_views.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """  User log out """
    session.pop('user', None)
    return (jsonify({'message': 'Logged out'}))


@app_views.route('/me', methods=['GET'], strict_slashes=False)
def me():
    """ Get loged in User """
    user = session.get('user')
    if user is not None:
        return (jsonify(user))
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
    user_data = new_user.to_dict()

    return jsonify(user_data), 201
