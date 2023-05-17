from flask import render_template
from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddFligtForm, SignUp, LogInForm, UpdateUserForm
from models import db, connect_db, User, Flight
from flask_bcrypt import Bcrypt
import requests
from datetime import datetime

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

token = "EYyOhTG6cC7zyG2F3ZwZLkcxpzjC"


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

            flash(f"Welcome Back, {user.first_name}!")
            session['user_id'] = user.id
            return redirect(f'/user/{user.id}')

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log out User"""

    if 'user_id' in session:
        session.pop('user_id')
        return redirect('/')


@app.route('/user/profile', methods=["POST", "GET"])
def edit_user():
    """UPDATE USER """

    form = UpdateUserForm()
    user = User.query.get_or_404(session['user_id'])

    if "user_id" not in session:
        flash("Please Login First!")
        return redirect('/login')

    if form.validate_on_submit():

        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data or user.username
            user.email = form.email.data or user.email
            user.first_name = form.first_name.data or user.first_name
            user.last_name = form.last_name.data or user.last_name

            db.session.commit()
            flash('Edits confirmed!')
            return redirect(f"/user/{session['user_id']}")

        flash('WRONG PASSWORD, Please Try Again!')

    return render_template('edit.html', form=form)


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """user details """
    user = User.query.get_or_404(user_id)

    flights = Flight.query.all()

    if "user_id" not in session:
        flash("Please Login First!")
        return redirect('/login')

    for flight in flights:

        flight.departure_time = flight.departure_time.strftime('%I:%M %p')
        flight.arrival_time = flight.arrival_time.strftime('%I:%M %p')
        flight.depature_date = flight.depature_date.strftime('%B %d, 20%y')
        flight.return_date = flight.return_date.strftime('%B %d, 20%y')
        flight.price = '${:,.2f}'.format(flight.price)

    if len(flights) == 0:
        flash("It's time to book your perfect flight!")

    return render_template('user_details.html', user=user, flights=flights)


#########################################################  FLIGHTS ##########################################################################

@app.route('/search', methods=["POST", "GET"])
def search_flights():
    """Search For Flight"""
    form = AddFligtForm()
    flights = []
    id = session.get('user_id')
    if "user_id" not in session:
        flash("Please Login First!")
        return redirect('/')

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
            'max': '4',
            'currencyCode': 'USD'
        }

        response = requests.get(
            f"{url}/shopping/flight-offers?", headers=headers, params=params)
        data = response.json()

        for flight in data['data']:
            origin = flight['itineraries'][0]['segments'][0]['departure']["iataCode"]
            departure_date = flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
                0]
            return_date = flight['itineraries'][1]['segments'][0]['arrival']['at'].split('T')[
                0]
            price = flight['price']['total']
            arrival = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
            adults = int(data['meta']['links']['self'].split(
                'adults=')[1].split('&')[0])

            departure_time = flight['itineraries'][0]['segments'][0]['departure']['at'].split(
                'T')[-1]
            arrival_time = flight['itineraries'][1]['segments'][0]['arrival']['at'].split('T')[
                -1]
            roundtrip = len(flight) > 1

            flight_info = {
                'origin': origin,
                'departure_date': departure_date,
                'return_date': return_date,
                'price': price,
                'arrival': arrival,
                'adults': adults,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'roundtrip': roundtrip
            }

            flights.append(flight_info)
            print(flights)

            session['flight_results'] = flights

        return redirect('/flights')
    else:
        return render_template('search.html', form=form, id=id)


@app.route('/flights')
def show_flights():
    """show flight """

    if "user_id" not in session:
        flash("Please Login First!")
    # Retrieve the flight results from the session
    flights = session.get('flight_results', [])

    id = session.get('user_id')

    session.pop('flight_results', None)

    for flight in flights:
        flight['departure_time'] = datetime.strptime(
            flight['departure_time'], '%H:%M:%S').strftime('%I:%M %p')
        flight['arrival_time'] = datetime.strptime(
            flight['arrival_time'], '%H:%M:%S').strftime('%I:%M %p')
        flight['departure_date'] = datetime.strptime(
            flight['departure_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        flight['return_date'] = datetime.strptime(
            flight['return_date'], '%Y-%m-%d').strftime('%B %d, %Y')

    if len(flights) == 0:
        flash('Look for your perfect flight now!')
        return redirect('/search')

    return render_template('flights.html', flights=flights)


@app.route('/booking', methods=['POST'])
def booking():
    """handle booking"""
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    departure_date = request.form.get('departure')
    return_date = request.form.get('return_date')
    price = request.form.get('price')
    adults = request.form.get('adults')
    departure_time = request.form.get('departure_time')
    roundtrip = request.form.get('roundtrip')
    arrival_time = request.form.get('arrival_time')

    """make instance of flight"""
    id = session.get('user_id')
    flight = Flight(
        origin=origin,
        destination=destination,
        departure_time=departure_time,
        arrival_time=arrival_time,
        depature_date=departure_date,

        return_date=return_date,
        adult=adults,
        price=float(price),
        user_id=id
        # Repla
    )
    db.session.add(flight)
    db.session.commit()
    flash('Flight Booked!!')

    return redirect(f'/user/{id}')


@app.route('/delete/ticket/<int:ticket_id>', methods=["GET", "POST"])
def delete_ticket(ticket_id):
    """Delete ticket"""
    id = session.get('user_id')

    flight = Flight.query.get_or_404(ticket_id)
    if "user_id" not in session:
        flash("Please Login First!")
    if request.method == "POST":
        db.session.delete(flight)
        db.session.commit()
        flash('Flight Deleted')
        return redirect(f'/user/{id}')

    return render_template('delete_ticket.html', flight=flight)
