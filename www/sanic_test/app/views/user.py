from sanic.exceptions import NotFound
from sanic.blueprints import Blueprint
from sanic.response import json
from ..db import Base, engine, Session
from ..models import User

user_bp = Blueprint('user', url_prefix='/users')


@user_bp.route("/", methods=["GET"])
async def all_users(request):
    sess = Session()
    users = list(map(lambda u: u.serialize(), sess.query(User)))
    return json(users), 201


@user_bp.route("/", methods=["POST"])
async def new_user(request):
    sess = Session()
    try:
        sess.add(User(**request.json))
        return json({"success": True})
    except Exception as e:
        return json({"success": False})


@user_bp.route("/<user_id:int>", methods=["GET"])
async def user(request, user_id):
    sess = Session()
    try:
        return json(sess.query(User).filter_by(id=user_id)[0].serialize())
    except IndexError:
        raise NotFound("no user found with id: " + str(user_id))


@user_bp.exception(NotFound)
async def not_found(request, exception):
    return json({"type": type(exception).__name__, "message": str(exception)})
