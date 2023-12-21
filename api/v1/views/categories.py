#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Categories"""
from models.category import Category
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_categories.yml')
def all_categories():
    """
    Retrieve the list of all Category objects
    """
    all_categories = storage.all(Category).values()
    list_categories = []
    for category in all_categories:
        list_categories.append(category.to_dict())

    return (jsonify(list_categories))


@app_views.route('/categories/<category_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/category/get_category.yml', methods=['GET'])
def get_category(category_id):
    """ Retrieves a category """
    category = storage.get(Category, category_id)

    if not category:
        abort(404, description="Category object not found")

    return jsonify(category.to_dict())


@app_views.route('/categories/<category_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/category/delete_category.yml', methods=['DELETE'])
def delete_category(category_id):
    """
    Deletes a category Object
    """
    category = storage.get(Category, category_id)

    if not category:
        abort(404, description="Category object not found")

    storage.delete(category)
    storage.save()

    return make_response(jsonify({'description': 'Category deleted successfully'}),
                         200)


@app_views.route('/categories', methods=['POST'], strict_slashes=False)
@swag_from('documentation/category/post_category.yml', methods=['POST'])
def create_category():
    """
    Create a new category
    """
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name of category")

    category = Category.get(data['name'])
    if not category:
        category = Category(**data)
        category.save()

    return make_response(jsonify(category.to_dict()), 201)


@app_views.route('/categories/<category_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/category/put_category.yml', methods=['PUT'])
def update_category(category_id):
    """
    Update a category
    """
    cat = storage.get(Category, category_id)

    if not cat:
        abort(404, description="Category object not found")

    data = request.get_json()
    if not data:
        abort(404, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(cat, key, value)

    cat.save()
    instance = cat.to_dict()

    return make_response(jsonify(instance), 200)
