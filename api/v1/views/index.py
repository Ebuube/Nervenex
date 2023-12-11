#!/usr/bin/python3
""" Index """
from models.user import User
from models.category import Category
from models.quiz import Quiz
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Category, Quiz, User]

    num_objs = {}
    for cls in classes:
        num_objs[cls.__name__] = storage.count(cls)

    return jsonify(num_objs)
