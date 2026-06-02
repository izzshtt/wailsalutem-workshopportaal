from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserForm(FlaskForm):
    """Form for creating or editing a user account."""

    naam = StringField('Naam', validators=[DataRequired(), Length(max=100)])
    email = StringField(
        'E-mailadres', validators=[DataRequired(), Email(), Length(max=150)]
    )
    rol = SelectField(
        'Rol',
        choices=[
            ('trainer', 'Trainer'),
            ('vrijwilliger', 'Vrijwilliger'),
            ('admin', 'Admin'),
            ('view-only', 'View-only'),
        ],
        validators=[DataRequired()]
    )
    # US-04: wachtwoord hashen bij opslaan
    wachtwoord = PasswordField(
        'Wachtwoord',
        validators=[Optional(), Length(min=6, max=100)]
    )
    telefoonnummer = StringField(
        'Telefoonnummer', validators=[Optional(), Length(max=20)]
    )
    leeftijdsrange = StringField(
        'Leeftijdsrange', validators=[Optional(), Length(max=20)]
    )
    submit = SubmitField('Opslaan')