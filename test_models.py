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
        self.assertEqual(event.status, "Pending First Approval")

    def test_first_approval(self):
        event = EventRequest("Workshop", "2024-10-05", "14:00", "Gothenburg", "XYZ Ltd")
        event.first_approval(approved=True, reviewer="SeniorCS")
        self.assertEqual(event.status, "Pending Financial Assessment")
        self.assertEqual(event.comments["first_approval"], "Approved by SeniorCS")

    def test_first_approval_rejection(self):
        event = EventRequest("Workshop", "2024-10-05", "14:00", "Gothenburg", "XYZ Ltd")
        event.first_approval(approved=False, reviewer="SeniorCS")
        self.assertEqual(event.status, "Rejected")
        self.assertEqual(event.comments["first_approval"], "Rejected by SeniorCS")

    def test_financial_comment(self):
        event = EventRequest("Expo", "2024-11-15", "09:00", "Malmo", "DEF Inc")
        event.first_approval(approved=True, reviewer="SeniorCS")
        event.financial_comment(comment="Budget approved", reviewer="FinManager")
        self.assertEqual(event.status, "Pending Final Approval")
        self.assertEqual(event.comments["financial"], "Commented by FinManager: Budget approved")

    def test_financial_comment_rejection(self):
        event = EventRequest("Expo", "2024-11-15", "09:00", "Malmo", "DEF Inc")
        event.first_approval(approved=True, reviewer="SeniorCS")
        event.financial_comment(comment="Budget too high", reviewer="FinManager")
        self.assertEqual(event.status, "Pending Final Approval")
        self.assertEqual(event.comments["financial"], "Commented by FinManager: Budget too high")

    def test_final_approval(self):
        event = EventRequest("Annual Gala", "2024-12-20", "18:00", "Lund", "LMN LLC")
        event.first_approval(approved=True, reviewer="SeniorCS")
        event.financial_comment(comment="Budget within limits", reviewer="FinManager")
        event.final_approval(approved=True, reviewer="AdminManager")
        self.assertEqual(event.status, "Approved")
        self.assertEqual(event.comments["final_approval"], "Approved by AdminManager")

    def test_final_approval_rejection(self):
        event = EventRequest("Annual Gala", "2024-12-20", "18:00", "Lund", "LMN LLC")
        event.first_approval(approved=True, reviewer="SeniorCS")
        event.financial_comment(comment="Budget within limits", reviewer="FinManager")
        event.final_approval(approved=False, reviewer="AdminManager")
        self.assertEqual(event.status, "Rejected")
        self.assertEqual(event.comments["final_approval"], "Rejected by AdminManager")

if __name__ == "__main__":
    unittest.main()