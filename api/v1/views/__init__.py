#!/usr/bin/python3
"""Blueprint for Nervenex API"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *    # noqa: E402
from api.v1.views.answers import *    # noqa: E402
from api.v1.views.attempts import *    # noqa: E402
from api.v1.views.categories import *    # noqa: E402
from api.v1.views.comments import *    # noqa: E402
from api.v1.views.posts import *    # noqa: E402
from api.v1.views.questions import *    # noqa: E402
from api.v1.views.quizzes import *    # noqa: E402
from api.v1.views.resources import *    # noqa: E402
from api.v1.views.threads import *    # noqa: E402
from api.v1.views.users import *    # noqa: E402
from api.v1.views.validating import *    # noqa: E402
from api.v1.views.auth import *    # noqa: E402
