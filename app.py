from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddFligtForm
from models import db, connect_db
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

token = "Ai14Y5IWLolKRZghsAIYCsdNcG9t"

headers = {'Authorization': f'Bearer {token}'}

url = 'https://test.api.amadeus.com/v2/'


@app.route('/')
def home():

    return render_template('home.html')


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
