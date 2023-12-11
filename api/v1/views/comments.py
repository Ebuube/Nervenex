#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for Comments"""
from models.comment import Comment
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/posts/<post_id>/comments',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/comment/get_comments_for_post.yml', methods=['GET'])
def get_comments_for_post(post_id):
    """
    Retrieves all comments for a specific post
    """
    try:
        post = storage.get(Post, post_id)

        if not post:
            abort(404, description="Post not found")

        comments = storage.all(Comment).values()
        post_comments = [comment.to_dict()
                         for comment in comments if comment.post_id == post_id]

        return jsonify(post_comments)
    except Exception as e:
        print("Exception: {}".format(e))
        return make_response(jsonify({'message': 'Something went wrong'}), 400)


@app_views.route('/comments/<comment_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/comment/get_comment.yml', methods=['GET'])
def get_comment(comment_id):
    """
    Retrieves a specific comment
    """
    try:
        comment = storage.get(Comment, comment_id)

        if not comment:
            abort(404, description="Comment not found")

        return jsonify(comment.to_dict())
    except Exception as e:
        print("Exception: {}".format(e))
        return make_response(jsonify({'message': 'Something went wrong'}), 400)


@app_views.route('/comments/<comment_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/comment/delete_comment.yml', methods=['DELETE'])
def delete_comment(comment_id):
    """
    Deletes a comment
    """
    try:
        comment = storage.get(Comment, comment_id)

        if not comment:
            abort(404, description="Comment not found")

        storage.delete(comment)
        storage.save()

        return make_response(
            jsonify({'message': 'Comment deleted successfully'}), 200)
    except Exception as e:
        print("Exception: {}".format(e))
        return make_response(jsonify({'message': 'Something went wrong'}), 400)


@app_views.route('/posts/<post_id>/comments',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/comment/create_comment.yml', methods=['POST'])
def create_comment(post_id):
    """
    Creates a comment for a specific post
    """
    try:
        data = request.get_json()

        if not data:
            abort(400, description="Not a JSON")

        if 'content' not in data:
            abort(400, description="Missing content")
        if 'author_id' not in data:
            abort(400, description="Missing author_id")

        # Check if the post exists
        post = storage.get(Post, post_id)
        if not post:
            abort(404, description="Post not found")

        # Create the comment
        data['post_id'] = post_id
        comment = Comment(**data)
        comment.save()

        return make_response(jsonify(comment.to_dict()), 201)
    except Exception as e:
        print("Exception: {}".format(e))
        return make_response(jsonify({'message': 'Something went wrong'}), 400)


@app_views.route('/comments/<comment_id>',
                 methods=['PUT'], strict_slashes=False)
@swag_from('documentation/comment/update_comment.yml', methods=['PUT'])
def update_comment(comment_id):
    """
    Updates a comment
    """
    try:
        comment = storage.get(Comment, comment_id)

        if not comment:
            abort(404, description="Comment not found")

        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        ignore = ['id', 'created_at', 'updated_at', 'post_id']

        for key, value in data.items():
            if key not in ignore:
                setattr(comment, key, value)
        storage.save()
        return make_response(jsonify(comment.to_dict()), 200)
    except Exception as e:
        print("Exception: {}".format(e))
        return make_response(jsonify({'message': 'Something went wrong'}), 400)
