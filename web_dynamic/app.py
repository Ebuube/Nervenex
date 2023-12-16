#!/usr/bin/python3
"""
Starts a Flask Web application to serve dynamic web page
"""
from uuid import uuid4
from models import storage
from models.quiz import Quiz
from models.thread import Thread
from flask import Flask, render_template, make_response, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


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


@app.route('/home', strict_slashes=False)
def home():
    """
    Return home page
    """
    quiz_cats = []
    for quiz in storage.all(Quiz).values():
        cat = quiz.category
        if cat not in quiz_cats:
            quiz_cats.append(cat)

    thread_cats = []
    for thread in storage.all(Thread).values():
        cat = thread.category
        if cat not in thread_cats:
            thread_cats.append(cat)
    return render_template('index.html', quiz_cats=quiz_cats,
            thread_cats=thread_cats)


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


if __name__ == "__main__":
    """
    Run app
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
