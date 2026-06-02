from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app import db
from app.decorators import role_required
from app.gebruikers import bp
from app.gebruikers.forms import UserForm
from app.models import User


def _email_exists(email_address, excluded_id=None):
    """Check if email is already in use by another user."""
    existing = User.query.filter_by(email=email_address.lower()).first()
    if existing is None:
        return False
    if excluded_id is not None and existing.id == excluded_id:
        return False
    return True


@bp.route('/')
@role_required(['admin'])
def overzicht():
    """Toon alle gebruikers, gefilterd op rol en/of naam/email — US-09."""
    role_filter = request.args.get('rol', '')
    zoekterm = request.args.get('zoek', '')

    query = User.query.order_by(User.name)

    if role_filter:
        query = query.filter_by(rol=role_filter)

    if zoekterm:
        query = query.filter(
            db.or_(
                User.name.ilike(f'%{zoekterm}%'),
                User.email.ilike(f'%{zoekterm}%')
            )
        )

    users = query.all()
    return render_template(
        'gebruikers/overzicht.html',
        gebruikers=users,
        huidige_rol=role_filter,
        zoekterm=zoekterm
    )


@bp.route('/nieuw', methods=['GET', 'POST'])
@role_required(['admin'])
def nieuw():
    form = UserForm()

    if request.method == 'GET' and request.args.get('rol'):
        form.rol.data = request.args.get('rol')

    if form.validate_on_submit():
        if _email_exists(form.email.data):
            flash('Dit e-mailadres is al in gebruik.', 'danger')
            return render_template(
                'gebruikers/formulier.html',
                form=form,
                titel='Gebruiker toevoegen'
            )

        user = User(
            name=form.naam.data,
            email=form.email.data.lower(),
            rol=form.rol.data,
            phone_number=form.telefoonnummer.data or None,
            age_range=form.leeftijdsrange.data or None,
        )
        if form.wachtwoord.data:
            user.set_password(form.wachtwoord.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Gebruiker {user.name} is aangemaakt.', 'success')
        return redirect(url_for('gebruikers.overzicht'))

    return render_template(
        'gebruikers/formulier.html',
        form=form,
        titel='Gebruiker toevoegen'
    )


@bp.route('/<int:gebruiker_id>/bewerken', methods=['GET', 'POST'])
@role_required(['admin'])
def bewerken(gebruiker_id):
    user = db.session.get(User, gebruiker_id) or abort(404)
    form = UserForm()

    if request.method == 'GET':
        form.naam.data = user.name
        form.email.data = user.email
        form.rol.data = user.rol
        form.telefoonnummer.data = user.phone_number
        form.leeftijdsrange.data = user.age_range

    if form.validate_on_submit():
        if _email_exists(form.email.data, excluded_id=user.id):
            flash('Dit e-mailadres is al in gebruik.', 'danger')
            return render_template(
                'gebruikers/formulier.html',
                form=form,
                titel='Gebruiker bewerken',
                gebruiker=user
            )

        user.name = form.naam.data
        user.email = form.email.data.lower()
        user.rol = form.rol.data
        user.phone_number = form.telefoonnummer.data or None
        user.age_range = form.leeftijdsrange.data or None

        if form.wachtwoord.data:
            user.set_password(form.wachtwoord.data)

        db.session.commit()
        flash(f'Gebruiker {user.name} is bijgewerkt.', 'success')
        return redirect(url_for('gebruikers.overzicht'))

    return render_template(
        'gebruikers/formulier.html',
        form=form,
        titel='Gebruiker bewerken',
        gebruiker=user
    )


@bp.route('/<int:gebruiker_id>/verwijderen', methods=['POST'])
@role_required(['admin'])
def verwijderen(gebruiker_id):
    user = db.session.get(User, gebruiker_id) or abort(404)

    # Trainer mag geen admin verwijderen — bewust inline (data-afhankelijk,
    
    if user.rol == 'admin' and not current_user.is_admin:
        flash('Je hebt geen toestemming om een admin te verwijderen.', 'danger')
        return redirect(url_for('gebruikers.overzicht'))

    # Niemand mag zijn eigen account verwijderen
    if user.id == current_user.id:
        flash('Je kunt je eigen account niet verwijderen.', 'danger')
        return redirect(url_for('gebruikers.overzicht'))

    if user.workshops:
        flash('Kan niet verwijderen: er zijn nog workshops gekoppeld.', 'danger')
        return redirect(url_for('gebruikers.overzicht'))
    
    name_copy = user.name
    db.session.delete(user)
    db.session.commit()
    flash(f'Gebruiker {name_copy} is verwijderd.', 'success')
    return redirect(url_for('gebruikers.overzicht'))