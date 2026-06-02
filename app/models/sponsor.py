from app import db


class Sponsor(db.Model):
    """Sponsor or partner organisation shown on the public page."""

    __tablename__ = 'sponsors'

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(150), nullable=False)
    website_url = db.Column(db.String(300), nullable=True)
    logo_bestandsnaam = db.Column(db.String(200), nullable=True)

    def heeft_logo(self) -> bool:
        """Return True when a logo file is linked to this sponsor."""
        return bool(self.logo_bestandsnaam)

    def heeft_website(self) -> bool:
        """Return True when a website URL is set for this sponsor."""
        return bool(self.website_url)

    def __repr__(self):
        return f'<Sponsor {self.naam}>'
