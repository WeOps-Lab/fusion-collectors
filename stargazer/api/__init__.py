from sanic import Blueprint

from stargazer.api.example import example_router
from stargazer.api.monitor import monitor_router

BLUEPRINTS = [monitor_router, example_router]

api = Blueprint.group(*BLUEPRINTS, url_prefix="/api")
