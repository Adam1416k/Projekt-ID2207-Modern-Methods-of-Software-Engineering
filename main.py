from models import User, Role, EventRequest
from auth import login, has_access

event_requests = []

def register_event(user):
    if has_access(user, Role.CUSTOMER_SERVICE):
        print("\n--- Register New Event ---")
        event_name = input("Event Name: ")
        date = input("Date (YYYY-MM-DD): ")
        time = input("Time (HH:MM): ")
        location = input("Location: ")
        client_name = input("Client Name: ")
        
        event = EventRequest(event_name, date, time, location, client_name)
        event_requests.append(event)
        print("Event request registered.")
    else:
        print("Access Denied. You do not have permission to register events.")

def main():
    print("Welcome to SEP Event Management System")
    username = input("Username: ")
    password = input("Password: ")
    
    user = login(username, password)
    
    if user:
        if has_access(user, Role.CUSTOMER_SERVICE):
            print("\nAvailable Actions:")
            print("1. Register New Event")
            choice = input("Choose an action (1): ")
            if choice == "1":
                register_event(user)
        else:
            print("No actions available for your role.")

if __name__ == "__main__":
    main()