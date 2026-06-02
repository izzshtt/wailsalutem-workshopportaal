from flask import Blueprint

bp = Blueprint('gebruikers', __name__, url_prefix='/gebruikers')

from app.gebruikers import routes  # noqa: E402, F401
