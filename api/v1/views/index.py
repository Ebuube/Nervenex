#!/usr/bin/python3
""" Index """
from models.answer import Answer
from models.attempt import Attempt
from models.authorized import Authorized
from models.category import Category
from models.comment import Comment
from models.post import Post
from models.question import Question
from models.quiz import Quiz
from models.resource import Resource
from models.thread import Thread
from models.user import User
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
    classes = [Answer, Attempt, Authorized, Category, Comment, Post,
               Question, Quiz, Resource, Thread, User]

    num_objs = {}
    for cls in classes:
        num_objs[cls.__name__] = storage.count(cls)

    return jsonify(num_objs)
