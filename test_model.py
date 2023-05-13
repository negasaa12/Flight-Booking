import unittest

from models import User, Flight, Airline


class UserTestCase(unittest.TestCase):

    def test_register(self):
        user = User.register("testuser", "password",
                             "John", "Doe", "test@example.com")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.password.startswith("$2b$"))

    def test_authenticate_valid(self):
        user = User.authenticate("testuser", "password")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")

    def test_authenticate_invalid(self):
        user = User.authenticate("testuser", "wrongpassword")
        self.assertFalse(user)

    def test_signup(self):
        user = User.signup("newuser", "new@example.com", "password")
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.password.startswith("$2b$"))


class FlightTestCase(unittest.TestCase):

    def test_flight_attributes(self):
        flight = Flight(
            origin="City A",
            destination="City B",
            depature_date="2023-05-15",
            return_date="2023-05-20",
            adult=2,
            price=200,
            departure_time="09:00:00",
            arrival_time="12:00:00"
        )
        self.assertEqual(flight.origin, "City A")
        self.assertEqual(flight.destination, "City B")
        self.assertEqual(flight.depature_date, "2023-05-15")
        self.assertEqual(flight.return_date, "2023-05-20")
        self.assertEqual(flight.adult, 2)
        self.assertEqual(flight.price, 200)
        self.assertEqual(flight.departure_time, "09:00:00")
        self.assertEqual(flight.arrival_time, "12:00:00")

    def test_flight_relationships(self):
        # Assuming you have User and Airline instances available for testing
        user = User(username="testuser", password="password",
                    email="test@example.com")
        airline = Airline(name="Test Airline")
        flight = Flight(
            origin="City A",
            destination="City B",
            depature_date="2023-05-15",
            return_date="2023-05-20",
            adult=2,
            price=200,
            departure_time="09:00:00",
            arrival_time="12:00:00",
            user=user,
            airline=airline
        )
        self.assertEqual(flight.user, user)
        self.assertEqual(flight.airline, airline)
