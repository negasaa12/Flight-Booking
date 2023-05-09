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

token = "GJe6um1QO901WVcctYvygeIcyG4M"

headers = {'Authorization': f'Bearer {token}'}

url = 'https://test.api.amadeus.com/v2/'


@app.route('/')
def home():

    return redirect('/signup')

    # return render_template('home.html')


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
            return redirect('/')

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/user/<int:user_id>')
def user_detail(user_id):

    if "user_id" not in session:
        flash("Please Login First!")
        return redirect('/signup')

    return render_template('user_details.html', user=user)


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
