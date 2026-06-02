from flask import Blueprint

# Blueprint voor de aanmeldformulier module.
# Alles onder deze module is bereikbaar via /aanmeldformulier.
bp = Blueprint(
    'aanmeldformulier', __name__, url_prefix='/aanmeldformulier'
)

# Importeert de routes pas na het aanmaken van de blueprint,
# zodat Flask de endpoints correct kan registreren.
from app.aanmeldformulier import routes  # noqa: E402, F401
