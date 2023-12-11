#!/usr/bin/python3
"""Blueprint for Nervenex API"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# shellcheck disable=E402
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.categories import *
from api.v1.views.validating import *
