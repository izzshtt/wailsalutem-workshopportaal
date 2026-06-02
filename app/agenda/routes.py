from flask_login import login_required
from datetime import date

from flask import render_template

from app.models import Workshop
from app.agenda import bp
from flask_login import login_required


@bp.route('/')
@login_required
def overzicht():
    """Display agenda with planned and completed workshops."""

    scheduled = (
        Workshop.query
        .filter(Workshop.date >= date.today())
        .order_by(Workshop.date.asc(), Workshop.start_time.asc())
        .all()
    )

    completed = (
        Workshop.query
        .filter(Workshop.date < date.today())
        .order_by(Workshop.date.desc(), Workshop.start_time.desc())
        .all()
    )

    return render_template(
        'agenda/overzicht.html',
        gepland=scheduled,
        afgerond=completed,
    )
