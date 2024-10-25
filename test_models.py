import unittest
from models import User, Role, EventRequest

class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User(username="cs_user", password="pass123", role=Role.CUSTOMER_SERVICE)
        self.assertEqual(user.username, "cs_user")
        self.assertEqual(user.role, Role.CUSTOMER_SERVICE)

    def test_user_password_verification(self):
        user = User(username="cs_user", password="pass123", role=Role.CUSTOMER_SERVICE)
        self.assertTrue(user.verify_password("pass123"))
        self.assertFalse(user.verify_password("wrong_pass"))

class TestEventRequestModel(unittest.TestCase):
    def test_event_request_creation(self):
        event = EventRequest("Conference", "2024-10-01", "10:00", "Stockholm", "ABC Corp")
        self.assertEqual(event.event_name, "Conference")
        self.assertEqual(event.client_name, "ABC Corp")
        self.assertEqual(event.status, "Pending")

if __name__ == "__main__":
    unittest.main()
