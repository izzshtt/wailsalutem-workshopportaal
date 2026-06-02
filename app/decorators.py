"""Autorisatie-decorators voor route-bescherming op basis van rol."""

from functools import wraps

from flask import render_template
from flask_login import current_user, login_required


def role_required(roles):
    """Sta toegang alleen toe aan ingelogde gebruikers met een rol uit `roles`.

    """
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.rol not in roles:
                return render_template('errors/403.html'), 403
            return view(*args, **kwargs)
        return wrapper
    return decorator
