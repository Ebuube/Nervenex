#!/usr/bin/python3
"""
Objects that handle all default RestFul API actions for Answers
"""
from models import storage
from models.answer import Answer
from models.attempt import Attempt
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/attempts/<attempt_id>/answers',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/answer/get_answers_by_attempt.yml')
def get_attempt_answers(attempt_id):
    """Get all answers for a specific attempt"""
    attempt = storage.get(Attempt, attempt_id)

    if not attempt:
        abort(404)

    list_answers = []
    for answer in attempt.answers:
        list_answers.append(answer.to_dict())

    return jsonify(list_answers)


@app_views.route('/attempts/<attempt_id>/answers',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/answer/post_answer.yml', methods=['POST'])
def create_answer(attempt_id):
    """Submitting answer for an attempt"""
    data = request.get_json()
    if not data or not isinstance(data, list):
        abort(400, description="Not a JSON or not a list")
    attempt = storage.get(Attempt, attempt_id)

    if not attempt:
        abort(404)

    for element in data:
        if 'question_id' not in element or 'value' not in element:
            abort(400, description="Missing required fields")

    for element in data:
        instance = Answer(question_id=element['question_id'],
                          attempt_id=attempt_id, value=element['value'])
        storage.save(instance)

    return make_response(
        jsonify({'message': 'Answers submitted successfully'}), 201)
