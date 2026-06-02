"""SQLAlchemy model for portal user accounts."""

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from app import db, login_manager

VALID_ROLES = ('admin', 'trainer', 'vrijwilliger', 'view-only')


class User(UserMixin, db.Model):
    """Portal user account (admin, trainer or volunteer)."""

    __allow_unmapped__ = True
    __tablename__ = 'gebruikers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('naam', db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column('wachtwoord_hash', db.String(256), nullable=True)
    rol = db.Column(
        db.String(20), nullable=False, default='trainer',
    )
    created_at = db.Column(
        'aangemaakt_op', db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    phone_number = db.Column('telefoonnummer', db.String(20), nullable=True)
    age_range = db.Column('leeftijdsrange', db.String(20), nullable=True)

    workshops = db.relationship(
        'Workshop', backref='trainer', lazy=True,
        foreign_keys='Workshop.trainer_id'
    )

    __table_args__ = (
        CheckConstraint(
            rol.in_(VALID_ROLES),
            name='ck_gebruikers_rol',
        ),
    )

    def set_password(self, password):
        """Hash en sla wachtwoord op."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vergelijk wachtwoord met opgeslagen hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """True wanneer de gebruiker een admin is."""
        return self.rol == 'admin'

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    """Laad gebruiker op ID — vereist door Flask-Login (US-02)."""
    return User.query.get(int(user_id))