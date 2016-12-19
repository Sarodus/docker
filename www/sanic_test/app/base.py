from sanic import Sanic
from sanic.response import json
from sanic.exceptions import NotFound
from .config import MyConfig


app = Sanic()
app.config = MyConfig()

from .db import Base, engine, session
from .models import User


@app.route("/", methods=["GET"])
async def hello(request):
    return json({'success': True})


@app.route("/users", methods=["GET"])
async def all_users(request):
    users = list(map(lambda u: u.serialize(), session.query(User)))
    return json(users)


@app.route("/user", methods=["POST"])
async def new_user(request):
    # TODO, validate
    try:
        session.add(User(**request.json))
        return json({"success": True})
    except Exception as e:
        return json({"success": False})


@app.route("/users/<user_id:int>", methods=["GET"])
async def user(request, user_id):
    # TODO, better msg
    try:
        return json(session.query(User).filter_by(id=user_id)[0].serialize())
    except IndexError:
        raise NotFound("no user found with id: " + str(user_id))


@app.exception(NotFound)
async def not_found(request, exception):
    return json({"type": type(exception).__name__, "message": str(exception)})
