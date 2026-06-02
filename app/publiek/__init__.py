from flask import Blueprint

bp = Blueprint('publiek', __name__, url_prefix='/publiek')

from app.publiek import routes  # noqa: E402, F401
