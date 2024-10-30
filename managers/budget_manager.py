import json
from datetime import datetime
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

    """ ------------  SERIALIZE AND DESERIALIZE BUDGET REQUEST FOR STORAGE TO JSON ------------ """

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
        # Instantiate BudgetRequest with deserialized data
        request = BudgetRequest(
            task_name=data["task_name"],
            requested_by=data["requested_by"],
            amount=data["amount"],
            status=data.get("status", "Pending"),  # Default to "Pending" if not provided
            fm_comment=data.get("fm_comment", "")  # Default to empty string if not provided
        )
        return request

    """ ------------  ADD BUDGET REQUEST ------------ """

    def add_request(self, request):
        """Add a new budget request and save."""
        self.requests.append(request)
        self.save_requests()  # Save immediately after adding a new request.


    # In BudgetManager
    def approve_request(self, request, approved):
        """Approves or rejects a budget request and saves the updated request."""
        if request.status == "Pending":
            request.status = "Approved" if approved else "Rejected"
            request.fm_comment = "Budget is approved" if approved else "Budget is denied"
            self.save_requests()  # Save the status update immediately
        return request




    def get_pending_budgets_for_fin_approval(self):
        """Returns a list of budget requests that are pending financial approval."""
        return [request for request in self.requests if request.status == "Pending"]
