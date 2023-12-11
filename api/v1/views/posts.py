#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Posts"""
from models.post import Post
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/posts', methods=['GET'], strict_slashes=False)
@swag_from('documentation/post/all_posts.yml')
def get_posts():
    """
    Retrieves the list of all post objects
    """
    all_posts = storage.all(Post).values()
    list_posts = []
    for post in all_posts:
        list_posts.append(post.to_dict())

    return jsonify(list_posts)


@app_views.route('/posts/<post_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/post/get_post.yml', methods=['GET'])
def get_post(post_id):
    """Retrieves a specific post"""
    post = storage.get(Post, post_id).first()

    if not post:
        abort(404, description="Post object not found")

    return jsonify(post.to_dict())


@app_views.route('/posts', methods=['POST'], strict_slashes=False)
@swag_from('documentation/post/post_post.yml', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'content' not in data:
        abort(400, description="Missing content")
    if 'thread_id' not in data:
        abort(400, description="Missing thread_id")

    if 'author_id' not in data:
        abort(400, description="Missing author_id")

    instance = Post(**data)
    instance.save()
    post = instance.to_dict()

    return make_response(jsonify(post), 201)


@app_views.route('/posts/<post_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/post/put_post.yml', methods=['PUT'])
def update_post(post_id):
    """Updates a post"""
    post = storage.get(Post, post_id).first()

    if not post:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(post, key, value)

    storage.save()

    return make_response(jsonify(post.to_dict()), 200)


@app_views.route('/posts/<post_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/post/delete_post.yml', methods=['DELETE'])
def delete_post(post_id):
    """Deletes a post"""
    post = storage.get(Post, post_id).first()

    if not post:
        abort(400, description="Not a JSON")

    storage.delete(post)
    storage.save()

    return make_response(jsonify({'message': 'Post deleted successfully'}),
                         200)
