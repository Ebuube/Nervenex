#!/usr/bin/python3
"""
Objects that handle all default RestFul API actions for Threads
"""
from models import storage
from models.thread import Thread
from models.category import Category
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/threads', methods=['GET'], strict_slashes=False)
@swag_from('documentation/thread/all_threads.yml')
def get_threads():
    """Retrieve all  threads"""
    all_threads = storage.all(Thread).values()
    list_threads = []
    for thread in all_threads:
        list_threads.append(thread.to_dict())

    return jsonify(list_threads)


@app_views.route('/categories/<category_id>/threads',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/thread/get_threads_by_category.yml')
def get_category_threads(category_id):
    """Get threada by category"""
    category = storage.get(Category, category_id)

    if not category:
        abort(404, description="Category not found")

    list_threads = []
    for thread in category.threads:
        list_threads.append(thread.to_dict())

    return jsonify(list_threads)


@app_views.route('/threads/<thread_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/thread/get_thread.yml', methods=['GET'])
def get_thread(thread_id):
    """Get specific thread"""
    thread = storage.get(Thread, thread_id)

    if not thread:
        abort(404, description="Thread not found")

    return jsonify(thread.to_dict())


@app_views.route('/threads', methods=['POST'], strict_slashes=False)
@swag_from('documentation/thread/post_thread.yml', methods=['POST'])
def create_thread():
    """Create a thread"""
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'title' not in data:
        abort(400, description="Missing title")
    if 'author_id' not in data:
        abort(400, description="Missing author_id")
    if 'category_id' not in data:
        abort(400, description="Missing category_id")

    author = storage.get(User, data['author_id'])
    category = storage.get(Category, data['category_id'])

    if not author or not category:
        abort(400, description="Invalid author_id or category_id")

    instance = Thread(**data)
    storage.save(instance)
    thread = instance.to_dict()

    return make_response(jsonify(thread), 201)


@app_views.route('/threads/<thread_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/thread/put_thread.yml', methods=['PUT'])
def update_thread(thread_id):
    """Update a thread"""
    thread = storage.get(Thread, thread_id)
    if not thread:
        abort(404, description="Thread not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(thread, key, value)

    storage.save()
    thread = thread.to_dict()

    return make_response(jsonify(thread), 200)


@app_views.route('/threads/<thread_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/thread/delete_thread.yml', methods=['DELETE'])
def delete_thread(thread_id):
    """Delete a thread"""
    thread = storage.get(Thread, thread_id)
    if not thread:
        abort(404, description="Thread not found")

    storage.delete(thread)
    storage.save()

    return make_response(
        jsonify({'message': 'Thread deleted successfully'}), 200)
