"""Login, registratie en logout routes."""

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app import db
from app.login import bp
from app.models import User


class LoginForm(FlaskForm):
    """Formulier voor inloggen."""
    email = StringField('E-mailadres', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Inloggen')


class RegistreerForm(FlaskForm):
    """Formulier voor registreren."""
    naam = StringField('Naam', validators=[DataRequired(), Length(max=100)])
    email = StringField('E-mailadres', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Wachtwoord',
        validators=[DataRequired(), Length(min=6)]
    )
    password2 = PasswordField(
        'Herhaal wachtwoord',
        validators=[DataRequired(), EqualTo('password', message='Wachtwoorden komen niet overeen.')]
    )
    submit = SubmitField('Registreren')


@bp.route('/', methods=['GET', 'POST'])
def login():
    """Toon loginformulier en verwerk inlogpoging."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower()
        ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash(f'Welkom terug, {user.name}!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        flash('Ongeldige inloggegevens.', 'danger')
    return render_template('auth/login.html', form=form)


@bp.route('/registreren', methods=['GET', 'POST'])
def registreren():
    """Toon registreerformulier en maak een nieuwe gebruiker aan."""
    form = RegistreerForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('Dit e-mailadres is al in gebruik.', 'danger')
            return render_template('auth/registreren.html', form=form)

        user = User(
            name=form.naam.data,
            email=form.email.data.lower(),
            rol='trainer',
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)
        flash(f'Account aangemaakt! Welkom, {user.name}.', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('auth/registreren.html', form=form)


@bp.route('/uitloggen')
@login_required
def logout():
    """Beëindig de sessie en stuur terug naar login."""
    logout_user()
    flash('Je bent uitgelogd.', 'success')
    return redirect(url_for('login.login'))