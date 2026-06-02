"""SQLAlchemy model for workshop sessions."""

from datetime import date, datetime, timezone

from app import db


class Workshop(db.Model):
    """Single workshop session given at a school."""

    __allow_unmapped__ = True
    __tablename__ = 'workshops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('naam', db.String(150), nullable=False)
    description = db.Column('beschrijving', db.Text, nullable=True)
    date: "date" = db.Column('datum', db.Date, nullable=False)
    start_time = db.Column('tijdstip', db.Time, nullable=False)
    end_time = db.Column('eindtijd', db.Time, nullable=True)
    location = db.Column('locatie', db.String(200), nullable=False)
    school = db.Column(db.String(150), nullable=False)
    participant_count = db.Column('aantal_deelnemers', db.Integer, nullable=False)
    max_participants = db.Column('max_deelnemers', db.Integer, nullable=True)
    duration = db.Column('duur', db.Integer, nullable=False)  # in minutes
    min_age = db.Column('leeftijd_min', db.Integer, nullable=True)
    max_age = db.Column('leeftijd_max', db.Integer, nullable=True)
    learning_outcomes = db.Column('leeruitkomsten', db.Text, nullable=True)  # JSON list
    trainer_id = db.Column(
        db.Integer, db.ForeignKey('gebruikers.id'), nullable=False
    )
    created_at = db.Column(
        'aangemaakt_op', db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    registrations = db.relationship(
        'Registration', backref='workshop', lazy=True, cascade='all, delete-orphan'
    )

    def is_completed(self) -> bool:
        """Return True when the workshop date is in the past."""
        if not self.date:
            return False
        return self.date < date.today()

    def is_scheduled(self) -> bool:
        """Return True when the workshop date is today or later."""
        if not self.date:
            return False
        return self.date >= date.today()

    def __repr__(self):
        return f'<Workshop {self.name} on {self.date}>'
