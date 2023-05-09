from flask import Flask, render_template, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddFligtForm, SignUp
from models import db, connect_db, User, Flight
from flask_bcrypt import Bcrypt
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flight_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "HELLO"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.secret_key = 'shhwewaeadsdwefafhh'

app.app_context().push()

connect_db(app)

token = "GJe6um1QO901WVcctYvygeIcyG4M"

headers = {'Authorization': f'Bearer {token}'}

url = 'https://test.api.amadeus.com/v2/'


@app.route('/')
def home():

    if session is 0:

        redirect('/signup')

    return render_template('home.html')


@app.route('/signup', methods=["POST", "GET"])
def signup():

    form = SignUp()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password,
                             email=email, first_name=first_name, last_name=last_name)

        db.session.commit()

    return render_template('signup.html', form=form)


@app.route('/search', methods=["POST", "GET"])
def show_flights():
    form = AddFligtForm()

    if form.validate_on_submit():
        origin = form.origin.data
        destination = form.destination.data
        date = form.date.data
        adults = form.people.data

    params = {'originLocationCode': 'SYD',
              'destinationLocationCode': 'NYC', "departureDate": "2023-10-10", 'adults': 1}
    response = requests.get(
        f"{url}/shopping/flight-offers?", headers=headers, params=params)

    data = response.json()

    return render_template('flights.html', form=form)


@app.route('/json')
def show_json():

    params = {'originLocationCode': 'SYD',
              'destinationLocationCode': 'NYC', "departureDate": "2023-10-10", 'adults': 1}

    response = requests.get(
        f"{url}/shopping/flight-offers?", headers=headers, params=params)

    data = response.json()

    return data
