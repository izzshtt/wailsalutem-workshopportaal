# Routes for creating, viewing, editing and deleting workshops and registrations

import json
from urllib.parse import quote_plus

from flask import abort, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import joinedload

from app import db
from app.models import User, Workshop
from app.workshops import bp
from app.workshops.forms import WorkshopForm
from app.decorators import role_required
from app.workshops.leeruitkomsten import LEARNING_OUTCOMES_GROUPS

INITIAL_PARTICIPANT_COUNT: int = 0


def _build_workshop_overview_data(workshops: list) -> list:
    """Convert a list of workshops into display data for the overview table."""
    rows: list = []

    for workshop in workshops:
        date_label = workshop.date.isoformat() if workshop.date else '—'
        row: dict = {
            'id': workshop.id,
            'naam': workshop.name,
            'datum': date_label,
            'locatie': workshop.location,
            'school': workshop.school,
            'status_label': 'Gepland' if workshop.is_scheduled() else 'Afgerond',
            'status_klasse': 'badge--gepland' if workshop.is_scheduled() else 'badge--afgerond',
            'trainer_naam': workshop.trainer.name if workshop.trainer else '—',
            'aantal_deelnemers': workshop.participant_count,
            'duur_label': f"{workshop.duration} min",
            'bewerken_url': url_for('workshops.bewerken', workshop_id=workshop.id),
            'verwijderen_url': url_for('workshops.verwijderen', workshop_id=workshop.id),
        }
        rows.append(row)

    return rows


@bp.route('/')
@role_required(['admin', 'trainer', 'vrijwilliger', 'view-only'])
def overzicht():
    """Show all workshops sorted by date."""
    workshops: list = (
        Workshop.query.options(joinedload(Workshop.trainer))
        .order_by(Workshop.date.desc())
        .all()
    )
    workshop_rows: list = _build_workshop_overview_data(workshops)

    return render_template(
        'workshops/overzicht.html',
        workshop_rijen=workshop_rows,
    )


@bp.route('/nieuw', methods=['GET', 'POST'])
@role_required(['admin', 'trainer'])
def nieuw():
    """Show the form for a new workshop and handle submission."""
    form: WorkshopForm = WorkshopForm()

    if form.validate_on_submit():
        trainer_id_param: str = request.form.get('trainer_id')
        trainer_id: int | None = int(trainer_id_param) if trainer_id_param else None

        if trainer_id is None:
            admin: User | None = User.query.filter_by(rol='admin').first()
            if admin:
                trainer_id = admin.id

        selected_outcomes: list = request.form.getlist('leeruitkomsten')

        workshop: Workshop = Workshop(
            name=form.naam.data,
            description=form.beschrijving.data,
            date=form.datum.data,
            start_time=form.tijdstip.data,
            end_time=form.eindtijd.data,
            location=form.locatie.data,
            school=form.school.data,
            participant_count=form.aantal_deelnemers.data or 0,
            duration=form.duur.data,
            min_age=form.leeftijd_min.data,
            max_age=form.leeftijd_max.data,
            learning_outcomes=json.dumps(selected_outcomes, ensure_ascii=False),
            trainer_id=trainer_id,
            # Kaart coördinaten
            latitude=form.latitude.data,
            longitude=form.longitude.data,
        )
        db.session.add(workshop)
        db.session.commit()
        flash('Workshop succesvol geregistreerd.', 'success')
        return redirect(url_for('workshops.overzicht'))

    trainers: list = User.query.filter_by(rol='trainer').all()

    return render_template(
        'workshops/formulier.html',
        form=form,
        titel='Workshop registreren',
        trainers=trainers,
        leeruitkomsten_groepen=LEARNING_OUTCOMES_GROUPS,
        geselecteerde_leeruitkomsten=[],
    )


@bp.route('/<int:workshop_id>/bewerken', methods=['GET', 'POST'])
@role_required(['admin', 'trainer'])
def bewerken(workshop_id: int):
    """Toon het bewerkformulier voor een bestaande workshop en verwerk wijzigingen."""
    workshop: Workshop = db.session.get(Workshop, workshop_id) or abort(404)
    form: WorkshopForm = WorkshopForm()

    if request.method == 'GET':
        form.naam.data = workshop.name
        form.beschrijving.data = workshop.description
        form.datum.data = workshop.date
        form.tijdstip.data = workshop.start_time
        form.eindtijd.data = workshop.end_time
        form.locatie.data = workshop.location
        form.school.data = workshop.school
        form.aantal_deelnemers.data = workshop.participant_count
        form.duur.data = workshop.duration
        form.leeftijd_min.data = workshop.min_age
        form.leeftijd_max.data = workshop.max_age
        # Kaart coördinaten laden
        form.latitude.data = workshop.latitude
        form.longitude.data = workshop.longitude

    if form.validate_on_submit():
        trainer_id_param: str = request.form.get('trainer_id')
        trainer_id: int | None = int(trainer_id_param) if trainer_id_param else None

        if trainer_id is None:
            admin: User | None = User.query.filter_by(rol='admin').first()
            if admin:
                trainer_id = admin.id

        workshop.name = form.naam.data
        workshop.description = form.beschrijving.data
        workshop.date = form.datum.data
        workshop.start_time = form.tijdstip.data
        workshop.end_time = form.eindtijd.data
        workshop.location = form.locatie.data
        workshop.school = form.school.data
        workshop.participant_count = form.aantal_deelnemers.data or 0
        workshop.duration = form.duur.data
        workshop.min_age = form.leeftijd_min.data
        workshop.max_age = form.leeftijd_max.data
        workshop.trainer_id = trainer_id
        workshop.learning_outcomes = json.dumps(
            request.form.getlist('leeruitkomsten'), ensure_ascii=False
        )
        # Kaart coördinaten opslaan
        workshop.latitude = form.latitude.data
        workshop.longitude = form.longitude.data

        db.session.commit()
        flash('Workshop bijgewerkt.', 'success')
        return redirect(url_for('workshops.overzicht'))

    trainers: list = User.query.filter_by(rol='trainer').all()
    selected_outcomes: list = (
        json.loads(workshop.learning_outcomes) if workshop.learning_outcomes else []
    )

    return render_template(
        'workshops/formulier.html',
        form=form,
        titel='Workshop bewerken',
        trainers=trainers,
        geselecteerde_trainer_id=workshop.trainer_id,
        leeruitkomsten_groepen=LEARNING_OUTCOMES_GROUPS,
        geselecteerde_leeruitkomsten=selected_outcomes,
    )


@bp.route('/<int:workshop_id>/verwijderen', methods=['POST'])
@role_required(['admin'])
def verwijderen(workshop_id: int):
    """Delete a workshop and all its related data from the database."""
    workshop: Workshop = db.session.get(Workshop, workshop_id) or abort(404)

    db.session.delete(workshop)
    db.session.commit()
    flash('Workshop verwijderd.', 'success')
    return redirect(url_for('workshops.overzicht'))