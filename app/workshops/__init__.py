from flask import Blueprint

bp = Blueprint('workshops', __name__, url_prefix='/workshops')

from app.workshops import routes  # noqa: E402, F401
