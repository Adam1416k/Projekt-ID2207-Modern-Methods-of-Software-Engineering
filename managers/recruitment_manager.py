import json
from models import RecruitmentRequest

class RecruitmentManager:
    def __init__(self, storage_file="recruitment_requests.json"):
        self.storage_file = storage_file
        self.requests = self.load_requests()

    def save_requests(self):
        """Save recruitment requests to a JSON file."""
        with open(self.storage_file, "w") as f:
            json.dump([req.to_dict() for req in self.requests], f)
        print("Recruitment requests saved to JSON.")

    def load_requests(self):
        """Load recruitment requests from a JSON file."""
        try:
            with open(self.storage_file, "r") as f:
                requests_data = json.load(f)
                print("Recruitment requests loaded from JSON.")
                return [RecruitmentRequest.from_dict(data) for data in requests_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("No recruitment requests file found or JSON error.")
            return []

    def add_request(self, request):
        """Add a new recruitment request and save."""
        self.requests.append(request)
        self.save_requests()

    def approve_request(self, request, comment):
        """Approve a recruitment request and add a financial manager's comment."""
        request.fm_status = "Approved"
        request.fm_comment = comment
        self.save_requests()
        print(f"Recruitment request for position '{request.position}' approved with comment: {comment}")

    def reject_request(self, request, comment):
        """Reject a recruitment request and add a financial manager's comment."""
        request.fm_status = "Rejected"
        request.fm_comment = comment
        self.save_requests()
        print(f"Recruitment request for position '{request.position}' rejected with comment: {comment}")

    
    #def get_pending_requests_for_financial_review(self):
        #"""Return recruitment requests pending financial review."""
       # return [request for request in self.requests if request.fm_status is None]
       
    def get_pending_requests_for_HR(self):
        """Return recruitment requests pending financial review."""
        return [request for request in self.requests if request.fm_status is None]
