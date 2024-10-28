class Role:
    CUSTOMER_SERVICE = "CustomerService"
    SENIOR_CUSTOMER_SERVICE = "SeniorCustomerService"
    FINANCIAL_MANAGER = "FinancialManager"
    ADMINISTRATIVE_MANAGER = "AdministrativeManager"
    PRODUCTION_MANAGER = "ProductionManager"
    TEAM_MEMBER = "TeamMember"

""" --------USER CLASS --------"""

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def verify_password(self, input_password):
        return self.password == input_password


""" --------EVENT CLASS --------"""

class EventRequest:
    def __init__(self, event_name, date, time, location, client_name):
        self.event_name = event_name
        self.date = date
        self.time = time
        self.location = location
        self.client_name = client_name
        self.status = "Pending First Approval"
        self.comments = {
            "first_approval": None,
            "financial": None,
            "final_approval": None
        }

    def first_approval(self, approved, reviewer):
        """Handles the first approval by Senior Customer Service."""
        if approved:
            self.status = "Pending Financial Assessment"
            self.comments["first_approval"] = f"Approved by {reviewer}"
        else:
            self.status = "Rejected"
            self.comments["first_approval"] = f"Rejected by {reviewer}"

    def financial_comment(self, comment, reviewer):
        """
        Adds a financial comment and updates the event status to Pending Final Approval.
        
        Args:
        - comment (str): The financial comment added by the Financial Manager.
        - reviewer (str): The Financial Manager's username.
        """
        if self.status == "Pending Financial Assessment":
            self.comments["financial"] = f"Commented by {reviewer}: {comment}"
            self.status = "Pending Final Approval"  # Move to next status

    def final_approval(self, approved, reviewer):
        """
        Handles final approval by the Administrative Manager.
        """
        if self.status == "Pending Final Approval":
            if approved:
                self.status = "Approved"  # Final approval, event is fully approved
                self.comments["final_approval"] = f"Approved by {reviewer}"
            else:
                self.status = "Rejected"
                self.comments["final_approval"] = f"Rejected by {reviewer}"

    """ --------TASK CLASS --------"""

class Task:
    def __init__(self, event, task_name, priority, assigned_team, status="Pending", created_by="", comments=None):
        self.event = event
        self.task_name = task_name
        self.priority = priority
        self.assigned_team = assigned_team
        self.status = status
        self.created_by = created_by
        self.comments = comments if comments else []

    """ --------RECRUITMENT CLASS --------"""

class RecruitmentRequest:
    def __init__(self, position, num_hires, urgency, justification, submitted_by, status="Pending", fm_status=None, fm_comment=None):
        self.position = position
        self.num_hires = num_hires
        self.urgency = urgency
        self.justification = justification
        self.submitted_by = submitted_by
        self.status = status
        self.fm_status = fm_status  # Financial Manager approval status (Approved/Rejected)
        self.fm_comment = fm_comment  # Financial Manager comment

    def to_dict(self):
        return {
            "position": self.position,
            "num_hires": self.num_hires,
            "urgency": self.urgency,
            "justification": self.justification,
            "submitted_by": self.submitted_by,
            "status": self.status,
            "fm_status": self.fm_status,
            "fm_comment": self.fm_comment,
        }

    @staticmethod
    def from_dict(data):
        return RecruitmentRequest(
            position=data["position"],
            num_hires=data["num_hires"],
            urgency=data["urgency"],
            justification=data["justification"],
            submitted_by=data["submitted_by"],
            status=data["status"],
            fm_status=data.get("fm_status"),
            fm_comment=data.get("fm_comment"),
        )