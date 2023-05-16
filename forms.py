from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, SelectField, PasswordField, DateField
from wtforms.validators import InputRequired, Email, Optional, DataRequired, URL, Length, Email


class AddFligtForm(FlaskForm):

    origin = StringField('Origin')

    destination = StringField('Destination')

    depature_date = DateField('Departure Date', format='%Y-%m-%d')

    return_date = DateField('Return Date', format='%Y-%m-%d')

    people = IntegerField('Adults')


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


class UpdateUserForm(FlaskForm):

    username = StringField('Username')
    email = StringField('E-mail')
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
