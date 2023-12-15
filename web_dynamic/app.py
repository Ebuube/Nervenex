#!/usr/bin/python3
"""
Starts a Flask Web application to serve dynamic web page
"""
from uuid import uuid4
from models import storage
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
def hbnb():
    """
    Return home page
    """
    return render_template('index.html',
                           cache_id=str(uuid4()))


if __name__ == "__main__":
    """
    Run app
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
