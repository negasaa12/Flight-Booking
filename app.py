from flask import render_template
from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddFligtForm, SignUp, LogInForm
from models import db, connect_db, User, Flight
from flask_bcrypt import Bcrypt
import requests

# CURR_USER_KEY = 'curr_user'

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

token = "GDY5er6L3e60IyVRvzbe8f6Qd70t"


headers = {'Authorization': f'Bearer {token}'}

url = 'https://test.api.amadeus.com/v2/'


@app.route('/')
def home():
    user_id = session.get('user_id')
    return render_template('home.html', user_id=user_id)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    """Sign Up Users"""

    form = SignUp()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password,
                             email=email, first_name=first_name, last_name=last_name)
        session['user_id'] = user.id
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    """Handle login Users"""

    form = LogInForm()

    if form.validate_on_submit():

        user = User.authenticate(form.username.data, form.password.data)

        if user:

            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.id
            return redirect(f'/user/{user.id}')

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """user details """
    user = User.query.get_or_404(user_id)

    flights = Flight.query.all()

    if "user_id" not in session:
        flash("Please Login First!")
        return redirect('/login')

    return render_template('user_details.html', user=user, flights=flights)


@app.route('/search', methods=["POST", "GET"])
def search_flights():
    """Search For Flight"""
    form = AddFligtForm()
    flights = []

    if "user_id" not in session:
        flash("Please Login First!")

    if form.validate_on_submit():
        origin = form.origin.data
        destination = form.destination.data
        departure_date = form.depature_date.data
        return_date = form.return_date.data
        adults = form.people.data

        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'returnDate': return_date,
            'adults': adults,
            'max': '3',
            'currencyCode': 'USD'
        }

        response = requests.get(
            f"{url}/shopping/flight-offers?", headers=headers, params=params)
        data = response.json()

        for flight in data['data']:
            origin = data['dictionaries']['locations']['EWR']['cityCode']
            departure_date = flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
                0]
            return_date = flight['itineraries'][1]['segments'][0]['arrival']['at'].split('T')[
                0]
            price = flight['price']['total']
            arrival = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
            adults = int(data['meta']['links']['self'].split(
                'adults=')[1].split('&')[0])

            flight_info = {
                'origin': origin,
                'departure_date': departure_date,
                'return_date': return_date,
                'price': price,
                'arrival': arrival,
                'adults': adults
            }

            flights.append(flight_info)

            session['flight_results'] = flights

        return redirect('/flights')
    else:
        return render_template('search.html', form=form)


@app.route('/flights')
def ahoflights():

    if "user_id" not in session:
        flash("Please Login First!")
    # Retrieve the flight results from the session
    flights = session.get('flight_results', [])
    id = session.get('user_id')

    session.pop('flight_results', None)

    return render_template('flights.html', flights=flights)


@app.route('/booking', methods=['POST'])
def booking():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_date = request.form.get('departure')
    return_date = request.form.get('return_date')
    price = request.form.get('price')
    adults = request.form.get('adults')

    id = session.get('user_id')
    flight = Flight(
        origin=origin,
        destination=destination,
        depature_date=departure_date,
        return_date=return_date,
        adult=adults,
        price=float(price),
        user_id=id
        # Repla
    )
    db.session.add(flight)
    db.session.commit()

    # Perform any desired processing or database operations with the retrieved data

    return redirect(f'/user/{id}')
