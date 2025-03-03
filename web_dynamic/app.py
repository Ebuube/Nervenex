#!/usr/bin/python3
"""
Starts a Flask Web application to serve dynamic web page
It needs to be run on its own server remotely
"""
import os
from datetime import datetime
from uuid import uuid4
from models import storage
from models.attempt import Attempt
from models.authorized import Authorized
from models.category import Category
from models.quiz import Quiz
from models.thread import Thread
from models.user import User
from flask import (Flask, render_template, make_response, jsonify,
                   redirect, g)
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['API_BASE_URL'] = os.getenv('API_BASE_URL')
app.config['WEB_BASE_URL'] = os.getenv('WEB_BASE_URL')


@app.before_request
def before_request():
    """
    Make some resoures available in context
    """
    g.api_base_url = app.config['API_BASE_URL']
    g.web_base_url = app.config['WEB_BASE_URL']


@app.errorhandler(Exception)
def not_found(error):
    """
    Generic error handler
    """
    if isinstance(error, HTTPException):
        # Specially handle HTTPExceptions
        message = error.__dict__
        message['status'] = error.code
        return make_response(jsonify(message), error.code)

    # Handle others errors
    print(error)
    return make_response(jsonify({"500": "Insternal server error"}), 500)


@app.teardown_appcontext
def close_db(error):
    """
    Remove the current SQLAlchemy session
    """
    storage.close()


def age(date):
    """
    Calculate the age of a datetime object

    Return a string about the age
    """
    if type(date) is not datetime:
        return ""

    one_hour = 60 * 60
    one_min = 60
    diff = datetime.now() - date
    if diff.days > 0:
        if diff.days == 1:
            return "1 day ago"
        else:
            return "{} days ago".format(diff.days)
    elif diff.seconds == one_hour or int(diff.seconds / one_hour) == 1:
        return "1 hour ago"
    elif diff.seconds > one_hour:
        return "{} hours ago".format(int(diff.seconds / one_hour))
    elif diff.seconds >= 2 * one_min:
        return "{} minutes ago".format(int(diff.seconds / one_min))
    else:
        return "just now"


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    """
    Redirect to home page
    """
    return redirect('https://nervenex.mailchimpsites.com/')


@app.route('/login', strict_slashes=False)
def login():
    """
    Return the login page
    """
    return render_template('log_in.html')


@app.route('/signup', strict_slashes=False)
def signup():
    """
    Return the signup page
    """
    return render_template('sign_up.html')


@app.route('/choose_quiz', strict_slashes=False)
def choose_quiz():
    """
    Return a page for choosing quizzes
    """
    quiz_cats = []
    quizzes = []
    for quiz in storage.all(Quiz).values():
        if not quiz.is_active:
            continue

        quiz.author.first_name = quiz.author.first_name.capitalize()
        quiz.author.last_name = quiz.author.last_name.capitalize()
        quiz.age = age(quiz.created_at)
        quizzes.append(quiz)
        cat = quiz.category
        if cat not in quiz_cats:
            quiz_cats.append(cat)

    return render_template('choose_quiz.html', quiz_cats=quiz_cats,
                           quizzes=quizzes)


@app.route('/quiz/<quiz_id>', strict_slashes=False)
def quiz(quiz_id):
    """
    Return a quiz to be taken by the user
    """
    quiz = storage.get(Quiz, quiz_id)
    if not quiz or not quiz.is_active:
        abort(404, description="Sorry, no such quiz..")

    return render_template('quiz.html', quiz=quiz)


def get_grade(value):
    """
    Award grade to a performance
    """
    if not value:
        return 'F'
    if not type(value) is int:
        return 'F'
    if value in range(70, 101):
        return 'A'
    elif value in range(60, 70):
        return 'B'
    elif value in range(50, 60):
        return 'C'
    elif value in range(45, 50):
        return 'D'
    elif value in range(40, 45):
        return 'E'
    else:
        return 'F'


@app.route('/correction/<attempt_id>', strict_slashes=False)
def correction(attempt_id):
    """
    View a correction for a particular attempt made
    """
    '''
    user = storage.get(User, user_id)
    if not user or not Authorized.is_auth(user):
        abort(401,
              description="Sorry, you are not allowed to access this attempt")
    '''
    attempt = storage.get(Attempt, attempt_id)
    if not attempt:
        abort(404, description="Sorry, no such attempt was made")

    questions = attempt.quiz.questions
    questions = []
    for answer in attempt.answers:
        questions.append(answer.question)

    answers = attempt.answers
    quiz = attempt.quiz
    time_hour = int(attempt.duration / 60)
    time_min = attempt.duration - (time_hour * 60)
    percent_score = int((attempt.score / len(attempt.answers)) * 100)
    grade = get_grade(percent_score)
    return render_template('correction.html', answers=answers,
                           questions=questions, quiz=quiz, time_min=time_min,
                           time_hour=time_hour, attempt=attempt,
                           percent_score=percent_score, grade=grade)


@app.route('/quiz_history/<user_id>', strict_slashes=False)
def quiz_history(user_id):
    """
    See all the user's prvious performance
    """
    user = storage.get(User, user_id)
    if not user or not Authorized.is_auth(user):
        abort(404, "Sorry, there is no such user")

    quizzes = []
    for attempt in user.attempts:
        if attempt.quiz not in quizzes:
            quizzes.append(attempt.quiz)
    return render_template('quiz_history.html', user=user, quizzes=quizzes)


@app.route('/create_quiz/<user_id>', strict_slashes=False)
def create_quiz(user_id):
    """
    Let user create a quiz
    """
    cats = storage.all(Category).values()
    return render_template('create_quizzes.html', categories=cats)


@app.route('/get_resources', strict_slashes=False)
def resources():
    """
    Render a list of the available resources
    """
    return render_template('resources.html')


if __name__ == "__main__":
    """
    Run app
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
