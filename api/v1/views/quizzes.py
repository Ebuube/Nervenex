#!/usr/bin/python3
"""
Objects that handle all default RestFul API actions for Quizzes
"""
from models import storage
from models.user import User
from models.quiz import Quiz
from models.category import Category
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/quizzes', methods=['GET'], strict_slashes=False)
@swag_from('documentation/quiz/all_quizzes.yml', methods=['GET'])
def all_quizzes():
    """
    Retrieve the list of all Quiz objects
    """
    all_quizzes = storage.all(Quiz).values()
    list_quizzes = []
    for quiz in all_quizzes:
        list_quizzes.append(quiz.to_dict())

    return (jsonify(list_quizzes))


@app_views.route('/quizzes/<quiz_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/quiz/get_quiz.yml', methods=['GET'])
def get_quiz(quiz_id):
    """"
    Retrieve a Quiz
    """
    quiz = storage.get(Quiz, quiz_id)

    if not quiz:
        abort(404, description="Quiz object not found")

    return jsonify(quiz.to_dict())


@app_views.route('/quizzes/<quiz_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/quiz/delete_quiz.yml', methods=['DELETE'])
def delete_quiz(quiz_id):
    """
    Delete a quiz instance
    """
    quiz = storage.get(Quiz, quiz_id)
    if not quiz:
        abort(404, description="Quiz object not found")

    storage.delete(quiz)
    storage.save()

    return make_response(
            jsonify({'message': 'Quiz deleted successfully'}), 200)


@app_views.route('/quizzes', methods=['POST'], strict_slashes=False)
@swag_from('documentation/quiz/post_quiz.yml', methods=['POST'])
def create_quiz():
    """
    Create a Quiz
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user id")
    else:
        user = storage.get(User, data['user_id'])
    if not user:
        abort(401, description="Unknown user")

    if 'category_id' not in data:
        abort(400, description="Missing category id")
    else:
        cat = storage.get(Category, data['category_id'])
    if not cat:
        abort(404, description="Category not found")

    if 'title' not in data:
        abort(400, description="Missing title")
    if 'description' not in data:
        abort(400, description="Missing description")
    if 'duration' not in data:
        abort(400, description="Missing duration")

    new = Quiz(**data)
    # Default: Every quiz is active or globally visible
    if 'is_active' not in data:
        new.is_active = True
    new.save()
    instance = new.to_dict()

    return make_response(jsonify(instance), 201)


@app_views.route('/quizzes/<quiz_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/quiz/put_quiz.yml', methods=['PUT'])
def update_quiz(quiz_id):
    """
    Update a Quiz
    """
    quiz = storage.get(Quiz, quiz_id)
    if not quiz:
        abort(404, description="Quiz object not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(quiz, key, value)
    quiz.save()

    return make_response(jsonify(quiz.to_dict()), 200)
