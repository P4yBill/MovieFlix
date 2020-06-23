from flask import (
    Blueprint
)
from .movies import Movies
from .users import Users
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# register the routes to api blueprint
Movies(api_bp)
Users(api_bp)
