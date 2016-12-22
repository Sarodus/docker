from sanic.response import json
from sanic.views import HTTPMethodView
from app.ext.api_model.sqla import ModelView
from ..db import Session
from ..models import User


def register_routes(app):
    ModelView(User, Session).register(app, url_prefix='/user')
