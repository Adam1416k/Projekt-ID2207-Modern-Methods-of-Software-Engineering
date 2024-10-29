class Role:
    CUSTOMER_SERVICE = "CustomerService"
    SENIOR_CUSTOMER_SERVICE = "SeniorCustomerService"
    FINANCIAL_MANAGER = "FinancialManager"
    ADMINISTRATIVE_MANAGER = "AdministrativeManager"
    PRODUCTION_MANAGER = "ProductionManager"
    TEAM_MEMBER = "TeamMember"
    HR_TEAM = "HumanResources"

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
    def __init__(self, position, num_hires, urgency, justification, submitted_by, status="Pending", fm_status=None, fm_comment=None, confirmed_start_date=None):
        self.position = position
        self.num_hires = num_hires
        self.urgency = urgency
        self.justification = justification
        self.submitted_by = submitted_by
        self.status = status
        self.fm_status = fm_status
        self.fm_comment = fm_comment
        self.confirmed_start_date = confirmed_start_date  # Start date of new hire

    def confirm_hire(self, confirmed_start_date):
        """Sets the confirmed start date and updates the status."""
        self.confirmed_start_date = confirmed_start_date
        self.status = "Confirmed Hire"

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
            "confirmed_start_date": self.confirmed_start_date
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
            confirmed_start_date=data.get("confirmed_start_date")
        )



    """-------- ADVERT CLASS ---------"""


class Advert(): 
    def __init__(self, position, start_date, coverage, experience, hr_comment, status = "Created"):
        #self.title = title
        self.position = position
        self.start_date = start_date
        self.coverage = coverage
        self.experience = experience
        self.hr_comment = hr_comment if hr_comment else []
        self.status = status




    """-------- Budget CLASS ---------"""


class BudgetRequest:
    def __init__(self, task_name, requested_by, amount, status="Pending", fm_comment=None):
        self.task_name = task_name
        self.requested_by = requested_by
        self.amount = amount
        self.status = status
        self.fm_comment = fm_comment if fm_comment else ""