# managers/event_manager.py
import json
from datetime import datetime
from models import EventRequest

class EventManager:
    def __init__(self, storage_file="events.json"):
        self.storage_file = storage_file
        self.events = self.load_events()  # Load events from file


    """------------ SET AND GET FROM JSON FILE ---------------"""

    def save_events(self):
        """Save events to a JSON file."""
        with open(self.storage_file, "w") as f:
            json.dump([self.serialize_event(event) for event in self.events], f)
        print("Events saved to JSON.")

    def load_events(self):
        """Load events from a JSON file."""
        try:
            with open(self.storage_file, "r") as f:
                events_data = json.load(f)
                print("Events loaded from JSON.")
                return [self.deserialize_event(event) for event in events_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("No events file found or JSON error.")
            return []



    """ ------------  ADDS NEW EVENT + error handler for duplicate names ------------  """ 

    def add_event(self, event):
        """
        Adds a new event if there is no event with the same name.
        """
        if self.is_duplicate_event(event.event_name):
            return False
        self.events.append(event)
        self.save_events()  # Ensure the new event is saved immediately
        return True

    def is_duplicate_event(self, event_name):
        """
        Checks if an event with the given name already exists.
        """
        return any(event.event_name == event_name for event in self.events)




    """ ------------  EVENT STATUS UPDATING ------------  """

    """ ------------  FIRST APPROVAL OF NEW EVENT ------------  """

    def first_approval(self, event, approved, reviewer):
        if event.status == "Pending First Approval":
            if approved:
                event.status = "Pending Financial Assessment"
                event.comments["first_approval"] = f"Approved by {reviewer}"
            else:
                event.status = "Rejected"
                event.comments["first_approval"] = f"Rejected by {reviewer}"
        return event


    """ ------------  FINANCIAL COMMENTING OF EVENT that has passed the first approval step ------------ """

    def financial_comment(self, event, approved, reviewer):
        if event.status == "Pending Financial Assessment":
            event.status = "Pending Final Approval"
            event.comments["financial"] = f"Commented by {reviewer}: {comment}"
        return event

    def add_financial_comment(self, event, comment, reviewer):
        """Adds a financial comment to an event and updates its status."""
        event.financial_comment(comment, reviewer)
        print(f"Updated event status: {event.status}, comment: {event.comments['financial']}")  # Debug print
        self.save_events()  # Save changes to JSON


    """ ------------ FINAL APPROVAL OF EVENT that has been given comment by financial manager------------   """

    def final_approval(self, event, approved, reviewer):
        if event.status == "Pending Final Approval":
            if approved:
                event.status = "Approved"
                event.comments["final_approval"] = f"Approved by {reviewer}"
            else:
                event.status = "Rejected"
                event.comments["final_approval"] = f"Rejected by {reviewer}"
        return event     



    """ ------------ EVENT LISTS FOR APPROVAL VIEWS ------------  

    ------------  FIRST APPROVAL VIEW ------------   """

    def get_pending_events_for_first_approval(self):
        """Returns a list of events that are pending first approval."""
        return [event for event in self.events if event.status == "Pending First Approval"]

    def get_approved_events_for_first_approval(self):
        """Returns a list of events that have been approved by SCS but not yet commented by financial manager."""
        return [event for event in self.events if event.status == "Pending Financial Assessment"]

    """ ------------  FINANCIAL ASSESSMENT VIEW ------------   """

    def get_pending_events_for_fin_com(self):
        """Returns a list of events that are pending financial assessment."""
        return [event for event in self.events if event.status == "Pending Financial Assessment"]

    def get_assessed_events_for_fin_com(self):
        """Returns a list of events that have been financially assessed but not yet final approved."""
        return [event for event in self.events if event.status == "Pending Final Approval"]

    
    """ ------------  FINAL APPROVAL VIEW ------------   """

    def get_pending_events_for_final_approval(self):
        """Returns a list of events that are pending final approval."""
        return [event for event in self.events if event.status == "Pending Final Approval"]

    def get_approved_events_for_final_approval(self):
        """Returns a list of events that have been finally approved."""
        return [event for event in self.events if event.status == "Approved"]




    """ ------------  SERIALIZE EVENT FOR STORAGE TO JSON------------   """

    def serialize_event(self, event):
        """Convert an EventRequest object to a serializable dictionary."""
        return {
            "event_name": event.event_name,
            "date": event.date.isoformat(),
            "time": event.time.isoformat(),
            "location": event.location,
            "client_name": event.client_name,
            "status": event.status,
            "comments": event.comments
        }

    def deserialize_event(self, data):
        """Convert a dictionary back to an EventRequest object."""
        # Parse date and time separately
        event_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        event_time = datetime.strptime(data["time"], "%H:%M:%S").time()
        
        event = EventRequest(
            event_name=data["event_name"],
            date=event_date,
            time=event_time,
            location=data["location"],
            client_name=data["client_name"]
        )
        event.status = data["status"]
        event.comments = data["comments"]
        return event
