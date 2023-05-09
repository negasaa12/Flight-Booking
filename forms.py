from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, SelectField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Optional, DataRequired, URL, Length, Email


class AddFligtForm(FlaskForm):

    origin = StringField('Origin', validators=[InputRequired(
        message='Please choose an Origin Destination')])

    destination = StringField('Destination', validators=[
                              InputRequired(message="Please choose a destination")])

    date = DateField('Date', format='%Y-%m-%d',
                     validators=[InputRequired(message='Please choose a date')])

    people = IntegerField('Adults', validators=[InputRequired(
        message="Please Choose the number of Adults")])


class SignUp(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])


class LogInForm(FlaskForm):
    """Form for logging in Users"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
