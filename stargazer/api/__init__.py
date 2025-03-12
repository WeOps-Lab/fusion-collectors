from sanic import Blueprint

from stargazer.api.example import example_router
from stargazer.api.colletc import collect_router

BLUEPRINTS = [collect_router, example_router]

api = Blueprint.group(*BLUEPRINTS, url_prefix="/api")