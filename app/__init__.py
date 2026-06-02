from flask import Flask, Response, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from config import Config

db: SQLAlchemy = SQLAlchemy()
csrf: CSRFProtect = CSRFProtect()
login_manager: LoginManager = LoginManager()


def create_app(config_class: type = Config) -> Flask:
    """Create and configure the Flask application."""

    app: Flask = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    login_manager.login_message = 'Log in om deze pagina te bekijken.'
    login_manager.login_message_category = 'warning'

    from app import models  # noqa: F401

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.workshops import bp as workshops_bp
    app.register_blueprint(workshops_bp)

    from app.agenda import bp as agenda_bp
    app.register_blueprint(agenda_bp)

    from app.gebruikers import bp as gebruikers_bp
    app.register_blueprint(gebruikers_bp)

    from app.publiek import bp as publiek_bp
    app.register_blueprint(publiek_bp)

    from app.aanmeldformulier import bp as aanmeldformulier_bp
    app.register_blueprint(aanmeldformulier_bp)

    # US-01/02/03 — login blueprint
    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.sponsors import bp as sponsors_bp
    app.register_blueprint(sponsors_bp)

    @app.route('/')
    def index() -> Response:
        return redirect(url_for('publiek.catalogus'))

    @app.before_request
    def make_session_permanent() -> None:
        session.permanent = True

    @app.errorhandler(403)
    def access_denied(error: Exception) -> tuple[str, int]:
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error: Exception) -> tuple[str, int]:
        return render_template('errors/404.html'), 404

    with app.app_context():
        db.create_all()
        _create_default_admin(app)
        _seed_sponsors()

    from app.commands import seed
    app.cli.add_command(seed)

    return app



def _seed_sponsors() -> None:
    """Seed the sponsors table once from the legacy JSON file."""
    import json
    import os
    from app.models.sponsor import Sponsor

    if Sponsor.query.first():
        return

    json_path = os.path.join(os.path.dirname(__file__), 'data', 'sponsors.json')
    if not os.path.exists(json_path):
        return

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        db.session.add(Sponsor(
            naam=item.get('naam', ''),
            website_url=item.get('website_url') or None,
            logo_bestandsnaam=item.get('logo_bestandsnaam') or None,
        ))
    db.session.commit()


def _create_default_admin(app: Flask) -> None:
    """Automatically create an admin account if none exists."""
    from werkzeug.security import generate_password_hash
    from app.models import User
    from sqlalchemy.exc import IntegrityError
    import secrets

    admin_email = app.config['ADMIN_EMAIL']
    if not User.query.filter_by(email=admin_email).first():
        password = secrets.token_urlsafe(12)
        admin_user = User(
            name='Admin',
            email=admin_email,
            password_hash=generate_password_hash(password),
            rol='admin'
        )
        db.session.add(admin_user)
        try:
            db.session.commit()
            app.logger.warning(
                'Admin account created. Email: %s — Password: %s',
                admin_email,
                password,
            )
        except IntegrityError:
            db.session.rollback()