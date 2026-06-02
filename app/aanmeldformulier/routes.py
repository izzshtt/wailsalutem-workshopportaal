"""Routes for the registration form vertical."""

from flask import abort, render_template
from sqlalchemy.orm import joinedload

from app import db
from app.models import Registration, Workshop
from app.aanmeldformulier import bp
from app.publiek.helpers import (
    _calculate_availability,
    _make_workshop_choice_options,
)


@bp.route('/overzicht')
def overzicht():
    """Show an overview of all registrations, sorted newest first."""
    registrations = (
        Registration.query
        .options(joinedload(Registration.workshop))
        .order_by(Registration.created_at.desc())
        .all()
    )
    return render_template('aanmeldformulier/overzicht.html', aanmeldingen=registrations)


@bp.route('/')
def formulier():
    """Show the registration form with workshop options."""
    workshops = Workshop.query.order_by(Workshop.date.asc()).all()
    available_spots_map, is_full_map = _calculate_availability(workshops)
    workshop_options = _make_workshop_choice_options(
        workshops=workshops,
        available_spots_map=available_spots_map,
        is_full_map=is_full_map,
    )
    return render_template(
        'aanmeldformulier/formulier.html',
        workshop_opties=workshop_options,
    )


@bp.route('/bevestiging/<int:aanmelding_id>')
def bevestiging(aanmelding_id: int):
    """Show the confirmation page for a saved registration."""
    registration = db.session.get(Registration, aanmelding_id)
    if not registration:
        abort(404)

    return render_template(
        'aanmeldformulier/bevestiging.html', aanmelding=registration
    )
