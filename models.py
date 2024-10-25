class Role:
    CUSTOMER_SERVICE = "CustomerService"
    SENIOR_CUSTOMER_SERVICE = "SeniorCustomerService"

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
        self.status = "Pending"
