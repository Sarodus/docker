from sanic import Sanic
from sanic.response import json
from sanic.exceptions import NotFound
from .config import MyConfig


app = Sanic()
app.config = MyConfig()

from .views.api import register_routes
register_routes(app)


@app.route("/", methods=["GET"])
async def hello(request):
    return json({'success': True})

@app.exception(NotFound)
async def not_found(request, exception):
    return json({"type": type(exception).__name__, "message": str(exception)})
