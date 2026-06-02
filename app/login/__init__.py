from flask import Blueprint

bp = Blueprint('login', __name__, url_prefix='/login')

from app.login import routes  # noqa: E402, F401