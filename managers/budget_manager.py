import json
from models import BudgetRequest

class BudgetManager:
    def __init__(self, storage_file="budget_requests.json"):
        self.storage_file = storage_file
        self.requests = self.load_requests()  # Load budget requests from file

    """------------ SET AND GET FROM JSON FILE ---------------"""

    def save_requests(self):
        """Save budget requests to a JSON file."""
        with open(self.storage_file, "w") as f:
            json.dump([self.serialize_request(request) for request in self.requests], f)
        print("Budget requests saved to JSON.")

    def load_requests(self):
        """Load budget requests from a JSON file."""
        try:
            with open(self.storage_file, "r") as f:
                requests_data = json.load(f)
                print("Budget requests loaded from JSON.")
                return [self.deserialize_request(data) for data in requests_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("No budget requests file found or JSON error.")
            return []

    """ ------------ ADD NEW BUDGET REQUEST ------------ """

    def add_request(self, request):
        """Add a new budget request and save."""
        self.requests.append(request)
        self.save_requests()  # Save immediately after adding a new request.

    """ ------------ BUDGET REQUEST STATUS UPDATING ------------ """

    def initial_review(self, request, approved, fm_comment):
        if request.status == "Pending":
            request.status = "Approved" if approved else "Rejected"
            request.fm_comment = fm_comment  # Save FM comment
            self.save_requests()  # Save changes immediately
        return request

    """ ------------ VIEW FILTERS FOR APPROVAL STAGES ------------ """

    def get_pending_budgets_for_fin_approval(self):
        """Returns a list of budget requests that are pending initial review."""
        return [request for request in self.requests if request.status == "Pending"]

    def get_approved_budgets(self):
        """Returns a list of budget requests that have been approved."""
        return [request for request in self.requests if request.status == "Approved"]

    def get_rejected_budgets(self):
        """Returns a list of budget requests that have been rejected."""
        return [request for request in self.requests if request.status == "Rejected"]

    """ ------------ SERIALIZE AND DESERIALIZE BUDGET REQUEST ------------ """

    def serialize_request(self, request):
        """Convert a BudgetRequest object to a serializable dictionary."""
        return {
            "task_name": request.task_name,
            "requested_by": request.requested_by,
            "amount": request.amount,
            "status": request.status,
            "fm_comment": request.fm_comment,
        }

    def deserialize_request(self, data):
        """Convert a dictionary back to a BudgetRequest object."""
        return BudgetRequest(
            task_name=data["task_name"],
            requested_by=data["requested_by"],
            amount=data["amount"],
            status=data.get("status", "Pending"),
            fm_comment=data.get("fm_comment", "")
        )
