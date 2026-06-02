"""SQLAlchemy model for workshop registrations."""

from datetime import datetime, timezone

from app import db


class Registration(db.Model):
    """Registration of a child for a workshop."""

    __allow_unmapped__ = True
    __tablename__ = 'aanmeldingen'

    id = db.Column(db.Integer, primary_key=True)
    workshop_id = db.Column(
        db.Integer, db.ForeignKey('workshops.id'), nullable=False
    )
    child_name = db.Column('naam_kind', db.String(150), nullable=False)
    age = db.Column('leeftijd', db.Integer, nullable=False)
    parent_name = db.Column('naam_ouder', db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column('telefoon', db.String(30), nullable=True)
    remarks = db.Column('opmerkingen', db.Text, nullable=True)
    created_at = db.Column(
        'aangemaakt_op', db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<Registration {self.child_name} for workshop {self.workshop_id}>'
