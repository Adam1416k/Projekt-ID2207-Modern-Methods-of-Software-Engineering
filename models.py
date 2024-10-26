
class Role:
    CUSTOMER_SERVICE = "CustomerService"
    SENIOR_CUSTOMER_SERVICE = "SeniorCustomerService"
    FINANCIAL_MANAGER = "FinancialManager"
    ADMINISTRATIVE_MANAGER = "AdministrativeManager"
    PRODUCTION_MANAGER = "ProductionManager"

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def verify_password(self, input_password):
        return self.password == input_password

class EventRequest:
    def __init__(self, event_name, date, time, location, client_name):
        self.event_name = event_name
        self.date = date
        self.time = time
        self.location = location
        self.client_name = client_name
        self.status = "Pending first approval"
        self.comments = {
            "first_approval": None,
            "financial": None,
            "final_approval": None
        }

    def first_approval(self, approved, reviewer):
        """
        Handles the first approval by Senior Customer Service.
        """
        if approved:
            self.status = "Pending Financial Assessment"
            self.comments["first_approval"] = f"Approved by {reviewer}"
        else:
            self.status = "Rejected"
            self.comments["first_approval"] = f"Rejected by {reviewer}"

    
    def financial_assessment(self, approved, budget_comments, reviewer):
        """
        Handles financial assessment by the Financial Manager.
        """
        if self.status == "Pending Financial Assessment":
            if approved:
                self.status = "Pending Final Approval"
                self.comments["financial"] = f"Approved by {reviewer}: {budget_comments}"
            else:
                self.status = "Rejected"
                self.comments["financial"] = f"Rejected by {reviewer}: {budget_comments}"

    def final_approval(self, approved, reviewer):
        """
        Handles final approval by the Administrative Manager.
        """
        if self.status == "Pending Final Approval":
            if approved:
                self.status = "Approved"
                self.comments["final_approval"] = f"Approved by {reviewer}"
            else:
                self.status = "Rejected"
                self.comments["final_approval"] = f"Rejected by {reviewer}"


class Task:
    def __init__(self, task_name, priority, assigned_team, created_by):
        self.task_name = task_name
        self.priority = priority
        self.assigned_team = assigned_team
        self.status = "Assigned"
        self.created_by = created_by


        




