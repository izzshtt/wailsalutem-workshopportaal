import json
from datetime import date
from urllib.parse import quote_plus

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy.orm import joinedload

from app import db
from app.models import Registration, Workshop
from app.models.sponsor import Sponsor
from app.publiek import bp
from app.publiek.constants import CATALOGUE_PAGE_LIMIT
from app.publiek.helpers import (
    _calculate_availability,
    _get_form_field,
    _make_catalogue_card_data,
    _make_workshop_choice_options,
)


@bp.route('/catalogus')
def catalogus():
    """Show the public workshop catalogue with upcoming workshops only."""
    # Get date filter from query parameters
    filter_date_str = request.args.get('datum')
    
    # DATABASE CALL 1: Fetch all workshops that are scheduled for today or later
    query = (
        Workshop.query
        .options(joinedload(Workshop.trainer))
        .filter(Workshop.date >= date.today())
    )
    
    # Apply date filter if provided
    if filter_date_str:
        try:
            # Parse the date from string format (YYYY-MM-DD)
            filter_date = date.fromisoformat(filter_date_str)
            query = query.filter(Workshop.date == filter_date)
        except (ValueError, TypeError):
            # Invalid date format, ignore filter
            pass
    
    workshops = (
        query
        .order_by(Workshop.date.asc())
        .limit(CATALOGUE_PAGE_LIMIT)
        .all()
    )
    available_spots_map, is_full_map = _calculate_availability(workshops)
    workshop_cards = _make_catalogue_card_data(
        workshops=workshops,
        available_spots_map=available_spots_map,
        is_full_map=is_full_map,
    )
    return render_template(
        'publiek/catalogus.html',
        workshop_kaarten=workshop_cards,
        selected_date=filter_date_str,
        sponsors=Sponsor.query.all(),
    )


@bp.route('/workshop/<int:workshop_id>')
def workshop_detail(workshop_id):
    """Show the public detail page for a single workshop."""
    workshop = Workshop.query.get_or_404(workshop_id)
    trainer_name = workshop.trainer.name if workshop.trainer else '-'
    location_encoded = quote_plus(workshop.location) if workshop.location else ''

    workshop_display = {
        'id': workshop.id,
        'naam': workshop.name,
        'datum': str(workshop.date),
        'tijdstip': str(workshop.start_time),
        'locatie': workshop.location or '-',
        'school': workshop.school,
        'trainer_naam': trainer_name,
        'aantal_deelnemers_label': f"{workshop.participant_count} personen",
        'duur_label': f"{workshop.duration} minuten",
        'heeft_locatie': bool(workshop.location),
        'locatie_encoded': location_encoded,
        'leeruitkomsten': json.loads(workshop.learning_outcomes) if workshop.learning_outcomes else [],
    }

    return render_template(
        'publiek/workshop-detail.html',
        workshop=workshop_display,
        vandaag=date.today(),
    )


@bp.route('/aanmelden', methods=['GET', 'POST'])
def aanmelden():
    """Show the public registration page and handle form submissions."""
    workshops = Workshop.query.order_by(Workshop.date.asc()).all()
    available_spots_map, is_full_map = _calculate_availability(workshops)
    workshop_options = _make_workshop_choice_options(
        workshops=workshops,
        available_spots_map=available_spots_map,
        is_full_map=is_full_map,
    )

    def _render_registration_page():
        return render_template(
            'publiek/aanmelden.html',
            workshop_opties=workshop_options,
        )

    if request.method == 'POST':
        workshop_id_raw = _get_form_field('workshop_id')
        child_name = _get_form_field('naam_kind')
        age_raw = _get_form_field('leeftijd')
        parent_name = _get_form_field('naam_ouder')
        email = _get_form_field('email').lower()
        phone = _get_form_field('telefoon', can_be_empty=True)
        remarks = _get_form_field('opmerkingen', can_be_empty=True)

        required_fields = [workshop_id_raw, child_name, age_raw, parent_name, email]
        if not all(required_fields):
            flash('Vul alle verplichte velden in.', 'warning')
            return _render_registration_page()

        try:
            workshop_id = int(workshop_id_raw)
            age = int(age_raw)
        except ValueError:
            flash('Ongeldige invoer bij workshop of leeftijd.', 'warning')
            return _render_registration_page()

        workshop = db.session.get(Workshop, workshop_id)
        if workshop is None:
            flash('De gekozen workshop bestaat niet meer.', 'danger')
            return _render_registration_page()

        if is_full_map.get(workshop.id, False):
            flash('Deze workshop is vol. Kies een andere workshop.', 'warning')
            return _render_registration_page()

        registration = Registration(
            workshop_id=workshop.id,
            child_name=child_name,
            age=age,
            parent_name=parent_name,
            email=email,
            phone=phone or None,
            remarks=remarks or None,
        )
        db.session.add(registration)
        db.session.commit()

        return redirect(url_for('publiek.bevestiging', aanmelding_id=registration.id))

    return _render_registration_page()


@bp.route('/bevestiging/<int:aanmelding_id>')
def bevestiging(aanmelding_id):
    """Show confirmation page after successful registration."""
    registration = Registration.query.get_or_404(aanmelding_id)
    return render_template('publiek/bevestiging.html', aanmelding=registration)


@bp.route('/privacybeleid')
def privacybeleid():
    """Show the privacy policy page."""
    return render_template('publiek/privacybeleid.html')


@bp.route('/voorwaarden')
def voorwaarden():
    """Show the terms and conditions page."""
    return render_template('publiek/voorwaarden.html')
