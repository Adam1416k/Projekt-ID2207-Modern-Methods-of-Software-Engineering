
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
    def __init__(self, event, task_name, priority, assigned_team, status="Pending", created_by=""):
        self.event = event
        self.task_name = task_name
        self.priority = priority
        self.assigned_team = assigned_team
        self.status = status
        self.created_by = created_by
