#!/usr/bin/python3
""" Flask Application """
from models import storage
from flask import Blueprint
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


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

app.config['SWAGGER'] = {
    'title': 'Nervenex Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('NERVENEX_API_HOST')
    print("host: {}".format(host))
    port = environ.get('NERVENEX_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    # app.run(host=host, port=port, threaded=True)
    app.run(debug=True, host=host, port=port, threaded=True)
