#!/usr/bin/python3
"""_summary_
"""
# api/v1/views/__init__.py
from flask import Blueprint
# from api.v1.views import states


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')



from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.users import *
