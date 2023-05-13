from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    "site Users"

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd

        )

        db.session.add(user)


class Flight(db.Model):

    __tablename__ = 'flights'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    origin = db.Column(db.String, nullable=False)

    destination = db.Column(db.String, nullable=False)

    depature_date = db.Column(db.Date, nullable=False)

    return_date = db.Column(db.Date, nullable=False)

    adult = db.Column(db.Integer, nullable=False)

    price = db.Column(db.Integer, nullable=False)

    departure_time = db.Column(db.Time, nullable=False)

    arrival_time = db.Column(db.Time, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    airline_id = db.Column(db.Integer, db.ForeignKey('airline.id'))

    airline = db.relationship('Airline', backref='flights')
    user = db.relationship('User', backref='flights',
                           primaryjoin="Flight.user_id == User.id")


class Airline(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(db.String, nullable=False)

    code = db.Column(db.String, nullable=False)

    """code and city Airport model"""
