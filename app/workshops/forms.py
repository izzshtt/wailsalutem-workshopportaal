from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Optional


class WorkshopForm(FlaskForm):
    """Form for creating or editing a workshop."""

    naam = StringField('Workshopnaam', validators=[DataRequired(message='Vul een naam in.'), Length(max=150)])
    beschrijving = TextAreaField('Beschrijving', validators=[Optional()])
    datum = DateField('Datum', validators=[DataRequired(message='Vul een datum in.')])
    tijdstip = TimeField('Starttijd', validators=[DataRequired(message='Vul een starttijd in.')])
    eindtijd = TimeField('Eindtijd', validators=[Optional()])
    locatie = StringField('Locatie', validators=[DataRequired(message='Vul een locatie in.'), Length(max=200)])
    school = StringField('School', validators=[DataRequired(message='Vul een school in.'), Length(max=150)])
    aantal_deelnemers = IntegerField('Aantal deelnemers', validators=[Optional(), NumberRange(min=0)], default=0)
    duur = IntegerField('Duur (minuten)', validators=[InputRequired(message='Vul een duur in minuten in.'), NumberRange(min=1)])
    leeftijd_min = IntegerField('Minimale leeftijd', validators=[Optional(), NumberRange(min=0)])
    leeftijd_max = IntegerField('Maximale leeftijd', validators=[Optional(), NumberRange(min=0)])
    latitude = FloatField('Breedtegraad (latitude)', validators=[Optional()])
    longitude = FloatField('Lengtegraad (longitude)', validators=[Optional()])
    submit = SubmitField('Opslaan')