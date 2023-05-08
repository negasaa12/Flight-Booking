from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, SelectField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Optional, DataRequired, URL


class AddFligtForm(FlaskForm):

    origin = StringField('Origin', validators=[InputRequired(
        message='Please choose an Origin Destination')])

    destination = StringField('Destination', validators=[
                              InputRequired(message="Please choose a destination")])

    date = DateField('Date', format='%Y-%m-%d',
                     validators=[InputRequired(message='Please choose a date')])

    people = IntegerField('Adults', validators=[InputRequired(
        message="Please Choose the number of Adults")])
