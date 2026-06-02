from flask import Blueprint

bp = Blueprint('agenda', __name__, url_prefix='/agenda')

from app.agenda import routes  
