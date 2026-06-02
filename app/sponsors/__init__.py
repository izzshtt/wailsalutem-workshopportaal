from flask import Blueprint

bp = Blueprint('sponsors', __name__, url_prefix='/sponsors')

from app.sponsors import routes  # noqa: E402, F401
