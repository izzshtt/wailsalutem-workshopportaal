import os

from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.decorators import role_required


from app import db
from app.models.sponsor import Sponsor
from app.sponsors import bp

LOGO_MAP = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
TOEGESTANE_EXTENSIES = {'png', 'jpg', 'jpeg', 'svg', 'webp', 'gif'}


def _toegestaan(bestandsnaam):
    return '.' in bestandsnaam and bestandsnaam.rsplit('.', 1)[1].lower() in TOEGESTANE_EXTENSIES


@bp.route('/')
@login_required
def overzicht():
    return render_template('sponsors/overzicht.html', sponsors=Sponsor.query.all())


@bp.route('/toevoegen', methods=['GET', 'POST'])
@role_required(['admin'])
def toevoegen():
    if request.method == 'POST':
        naam = request.form.get('naam', '').strip()
        website_url = request.form.get('website_url', '').strip() or None
        logo_bestand = request.files.get('logo')

        if not naam:
            flash('Naam is verplicht.', 'warning')
            return render_template('sponsors/formulier.html', titel='Sponsor toevoegen', sponsor=None)

        logo_bestandsnaam = None
        if logo_bestand and logo_bestand.filename and _toegestaan(logo_bestand.filename):
            logo_bestandsnaam = secure_filename(logo_bestand.filename)
            logo_bestand.save(os.path.join(LOGO_MAP, logo_bestandsnaam))

        sponsor = Sponsor(naam=naam, website_url=website_url, logo_bestandsnaam=logo_bestandsnaam)
        db.session.add(sponsor)
        db.session.commit()
        flash(f'Sponsor "{naam}" toegevoegd.', 'success')
        return redirect(url_for('sponsors.overzicht'))

    return render_template('sponsors/formulier.html', titel='Sponsor toevoegen', sponsor=None)


@bp.route('/<int:sponsor_id>/bewerken', methods=['GET', 'POST'])
@role_required(['admin'])
def bewerken(sponsor_id):
    sponsor = Sponsor.query.get_or_404(sponsor_id)

    if request.method == 'POST':
        naam = request.form.get('naam', '').strip()
        website_url = request.form.get('website_url', '').strip() or None
        logo_bestand = request.files.get('logo')

        if not naam:
            flash('Naam is verplicht.', 'warning')
            return render_template('sponsors/formulier.html', titel='Sponsor bewerken', sponsor=sponsor)

        if logo_bestand and logo_bestand.filename and _toegestaan(logo_bestand.filename):
            logo_bestandsnaam = secure_filename(logo_bestand.filename)
            logo_bestand.save(os.path.join(LOGO_MAP, logo_bestandsnaam))
            sponsor.logo_bestandsnaam = logo_bestandsnaam

        sponsor.naam = naam
        sponsor.website_url = website_url
        db.session.commit()
        flash(f'Sponsor "{naam}" bijgewerkt.', 'success')
        return redirect(url_for('sponsors.overzicht'))

    return render_template('sponsors/formulier.html', titel='Sponsor bewerken', sponsor=sponsor)


@bp.route('/<int:sponsor_id>/verwijderen', methods=['POST'])
@role_required(['admin'])
def verwijderen(sponsor_id):
    sponsor = Sponsor.query.get_or_404(sponsor_id)
    db.session.delete(sponsor)
    db.session.commit()
    flash(f'Sponsor "{sponsor.naam}" verwijderd.', 'success')
    return redirect(url_for('sponsors.overzicht'))
