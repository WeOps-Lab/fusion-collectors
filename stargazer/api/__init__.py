from sanic import Blueprint
from api.example import example_router

api = Blueprint.group(example_router, url_prefix="/api")
