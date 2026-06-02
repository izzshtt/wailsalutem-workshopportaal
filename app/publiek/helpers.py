from datetime import date, time
from urllib.parse import quote_plus

from flask import request
from sqlalchemy import func

from app import db
from app.models import Registration, Workshop
from app.publiek.constants import DUTCH_MONTHS, DUTCH_WEEKDAYS


def _format_workshop_date_time_location(
    workshop_date: date,
    start_time: time,
    end_time: time | None,
    location: str
) -> str:
    """Format workshop date, time and location into display format."""
    weekday_en = workshop_date.strftime('%A')
    weekday_nl = DUTCH_WEEKDAYS.get(weekday_en, weekday_en)

    day = workshop_date.day
    month_en = workshop_date.strftime('%B')
    month_nl = DUTCH_MONTHS.get(month_en, month_en)

    time_str = start_time.strftime('%H:%M') if start_time else ''

    if end_time:
        end_time_str = end_time.strftime('%H:%M')
        time_range = f"{time_str}-{end_time_str}"
    else:
        time_range = time_str

    return f"{weekday_nl} {day} {month_nl} • {time_range} {location}"


def _get_form_field(field_name: str, can_be_empty: bool = False) -> str:
    """Retrieve and clean a form field value from request."""
    value = request.form.get(field_name, '').strip()
    return value if value or can_be_empty else ''


def _calculate_availability(workshops: list):
    """Calculate available spots and full status for each workshop."""
    workshop_ids = [workshop.id for workshop in workshops]
    registrations_per_workshop = {}

    if workshop_ids:
        # DATABASE CALL 2: Count how many registrations exist for each workshop
        rows = (
            db.session.query(
                Registration.workshop_id,
                func.count(Registration.id)
            )
            .filter(Registration.workshop_id.in_(workshop_ids))
            .group_by(Registration.workshop_id)
            .all()
        )
        for workshop_id, count in rows:
            registrations_per_workshop[workshop_id] = int(count)

    available_spots_map = {}
    is_full_map = {}

    for workshop in workshops:
        if workshop.max_participants is None:
            available_spots_map[workshop.id] = None
            is_full_map[workshop.id] = False
            continue

        new_registrations = registrations_per_workshop.get(workshop.id, 0)
        available_spots = max(0, workshop.max_participants - new_registrations)

        available_spots_map[workshop.id] = available_spots
        is_full_map[workshop.id] = available_spots == 0

    return available_spots_map, is_full_map


def _determine_avatar_class(workshop_name: str) -> str:
    """Determine CSS class for workshop avatar based on title keywords."""
    name_lower = workshop_name.lower()

    avatar_keywords = {
        'ws-avatar--ai': ('ai',),
        'ws-avatar--robot': ('robot',),
        'ws-avatar--vr': ('vr', 'virtual'),
        'ws-avatar--code': ('program', 'code'),
    }

    for css_class, keywords in avatar_keywords.items():
        for keyword in keywords:
            if keyword in name_lower:
                return css_class

    return 'ws-avatar--default'


def _make_catalogue_card_data(workshops, available_spots_map, is_full_map):
    """Prepare plain display data for the catalogue cards."""
    cards = []

    for workshop in workshops:
        available_spots = available_spots_map.get(workshop.id)
        is_full = is_full_map.get(workshop.id, False)

        card = {
            'id': workshop.id,
            'naam': workshop.name,
            'avatar_klasse': _determine_avatar_class(workshop.name),
            'avatar_letter': (workshop.name[:1] or '?').upper(),
            'school': workshop.school,
            'locatie': workshop.location,
            'heeft_locatie': bool(workshop.location),
            'heeft_beschrijving': bool(workshop.description),
            'beschrijving': workshop.description or '',
            'heeft_leeftijd': bool(workshop.min_age or workshop.max_age),
            'leeftijd_label': f"{workshop.min_age or '?'}-{workshop.max_age or '?'} jaar",
            'heeft_duur': bool(workshop.duration),
            'duur_label': f"{workshop.duration}min" if workshop.duration else '',
            'heeft_trainer': bool(workshop.trainer),
            'trainer_naam': workshop.trainer.name if workshop.trainer else '',
            'datum_tijd_locatie_label': _format_workshop_date_time_location(
                workshop.date, workshop.start_time, workshop.end_time,
                workshop.location
            ),
            'is_vol': is_full,
            'vrije_plekken': available_spots,
            'vrije_plekken_label': (
                f"{available_spots} plekken vrij"
                if available_spots is not None else 'Beschikbaar'
            ),
            'mailto_subject': quote_plus(f"Interesse in {workshop.name}"),
        }
        cards.append(card)

    return cards


def _make_workshop_choice_options(workshops, available_spots_map, is_full_map):
    """Build rendering-ready select options for the registration form."""
    options = []

    for workshop in workshops:
        available_spots = available_spots_map.get(workshop.id)
        is_full = is_full_map.get(workshop.id, False)

        label = f"{workshop.name} - {workshop.date}"
        if is_full:
            label = f"{label} (Vol)"
        elif available_spots is not None:
            label = f"{label} ({available_spots} plekken vrij)"

        options.append(
            {
                'id': workshop.id,
                'label': label,
                'disabled': is_full,
            }
        )

    return options
