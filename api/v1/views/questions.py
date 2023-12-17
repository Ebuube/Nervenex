#!/usr/bin/python3
"""
Objects that handle all default RestFul API actions for Questions
"""
from models import storage
from models.question import Question
from models.quiz import Quiz
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/quizzes/<quiz_id>/questions/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/question/all_questions.yml', methods=['GET'])
def all_questions_from_quiz(quiz_id):
    """
    Retrieve all question instances from a Quiz
    """
    quiz = storage.get(Quiz, quiz_id)
    if not quiz or not quiz.is_active:
        abort(404, description="Quiz object not found")

    all_questions = []
    for question in quiz.questions:
        all_questions.append(question.to_dict())

    return jsonify(all_questions)


@app_views.route('/questions/<question_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/question/get_question.yml', methods=['GET'])
def get_question(question_id):
    """
    Retrieve a particular Question based on Id
    """
    question = storage.get(Question, question_id)
    if not question:
        abort(404, description="Question object not found")

    return jsonify(question.to_dict())


@app_views.route('/questions/<question_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/question/delete_question.yml', methods=['DELETE'])
def delete_question(question_id):
    """
    Delete a Question instance
    """
    question = storage.get(Question, question_id)
    if not question:
        abort(404, description="Question object not found")

    storage.delete(question)
    storage.save()

    return make_response(
            jsonify({'description': 'Question deleted successfully'}), 200)


@app_views.route('/questions', methods=['POST'], strict_slashes=False)
@swag_from('documentation/question/post_question.yml', methods=['POST'])
def create_question():
    """
    Create a Question
    """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'quiz_id' not in data:
        abort(400, description="Missing quiz id")
    else:
        quiz = storage.get(Quiz, data['quiz_id'])
        if not quiz:
            abort(404, description="Quiz object not found")

    if 'content' not in data:
        abort(400, description="Missing content")
    if 'option_a' not in data:
        abort(400, description="Missing option a")
    if 'option_b' not in data:
        abort(400, description="Missing option b")
    if 'option_c' not in data:
        abort(400, description="Missing option c")
    if 'option_d' not in data:
        abort(400, description="Missing option d")
    if 'correct_answer' not in data:
        abort(400, description="Missing corect answer")
    if 'explanation' not in data:
        abort(400, description="Missing explanation")

    new = Question(**data)
    new.save()

    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/questions/<question_id>',
                 methods=['PUT'],  strict_slashes=False)
@swag_from('documentation/question/put_question.yml', methods=['PUT'])
def update_question(question_id):
    """
    Update a question
    """
    question = storage.get(Question, question_id)
    if not question:
        abort(404, description="Question object not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(question, key, value)
    question.save()

    return make_response(jsonify(question.to_dict()), 200)
