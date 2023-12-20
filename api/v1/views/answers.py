#!/usr/bin/python3
"""
Objects that handle all default RestFul API actions for Answers
"""
from models import storage
from models.answer import Answer
from models.attempt import Attempt
from models.authorized import Authorized
from models.question import Question
from models.quiz import Quiz
from models.user import User
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
        jsonify({'description': 'Answers submitted successfully'}), 201)


def grade_answers(attempt=None, answers=None):
    """
    Grade the answers supplied by this user and save them

    Return the score
    """
    if not attempt or not answers:
        return 0

    if not type(answers) == dict:
        return 0

    score = 0
    for question, ans in answers.items():
        # record performance
        question = storage.get(Question, question)
        if not question:
            # Question not found -> Mark the recognized questions
            continue
        u_answer = Answer()
        u_answer.question_id = question.id
        u_answer.attempt_id = attempt.id
        u_answer.value = ans
        u_answer.save()
        if u_answer.value == question.correct_answer:
            score = score + 1

    return score


@app_views.route('/submit/<user_id>/quiz/<quiz_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/answer/submit.yml', methods=['POST'])
def submit(user_id, quiz_id):
    """
    A better way to submit answers for a quiz
    Attempt is automatically created
    Format:
    {
        "duration": <int - in minutes>,
        "ans_per_question": {
            # For each question
            "question_id": <int - answer number>
        }
    }
    """
    # User authentication
    user = storage.get(User, user_id)
    if not user:
        abort(401, "Sorry, there is no such user 😞")
    if not Authorized.is_auth(user):
        abort(401, "Sorry, please log in to see your performance 🤗")

    quiz = storage.get(Quiz, quiz_id)
    if not quiz:
        abort(401, "Sorry, there is no such quiz 😞")

    # Validation of data format
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, description="Invalid submision format")

    requirements = ['duration', 'ans_per_question']
    for item in requirements:
        if item not in data:
            abort(400, description="Missing required field -> {}".format(item))
        if item == 'ans_per_question' and not isinstance(data[item], dict):
            abort(400, description="Invalid answer format")


    # Register performance
    attempt = Attempt()
    attempt.user_id = user.id
    attempt.quiz_id = quiz.id
    attempt.score = 0
    attempt.duration = data['duration']
    attempt.save()
    attempt.score = grade_answers(attempt=attempt,
                                  answers=data['ans_per_question'])
    attempt.save()
    return make_response(jsonify(attempt.to_dict()), 201)
