# gui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from datetime import datetime, date, time
from models import EventRequest, Role
from managers.event_manager import EventManager
from auth import login, has_access

class EventOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Organizer")
        self.event_manager = EventManager()
        self.current_user = None
        self.create_login_screen()


    def create_login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.handle_login).pack()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = login(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Login Successful", f"Welcome, {user.role}!")
            self.navigate_to_role_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def navigate_to_role_screen(self):
        if has_access(self.current_user, Role.CUSTOMER_SERVICE):
            self.create_event_registration_screen()
        elif has_access(self.current_user, Role.SENIOR_CUSTOMER_SERVICE):
            self.create_first_approval_screen()
        else:
            messagebox.showerror("Access Denied", "You do not have access to any screens.")

    def logout(self):
        """Logs out the current user and returns to the login screen."""
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out.")
        self.create_login_screen()  # Redirect to login screen


    def create_event_registration_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Register Event").pack()
        
        self.event_name_entry = tk.Entry(self.root)
        self.event_name_entry.insert(0, "Event Name")
        self.event_name_entry.pack()

        self.date_entry = tk.Entry(self.root)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.pack()

        self.time_entry = tk.Entry(self.root)
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.pack()

        self.location_entry = tk.Entry(self.root)
        self.location_entry.insert(0, "Location")
        self.location_entry.pack()

        self.client_name_entry = tk.Entry(self.root)
        self.client_name_entry.insert(0, "Client Name")
        self.client_name_entry.pack()

        tk.Button(self.root, text="Register Event", command=self.register_event).pack()

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)


    def register_event(self):
        event_name = self.event_name_entry.get()
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()
        location = self.location_entry.get()
        client_name = self.client_name_entry.get()
        
        # Convert date and time
        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            event_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter date and time in correct format.")
            return
        
        # Create the event object
        event = EventRequest(event_name, event_date, event_time, location, client_name)
        
        # Check for duplicate events
        if not self.event_manager.add_event(event):
            messagebox.showerror("Duplicate Event", f"An event with the name '{event_name}' already exists.")
            return
        
        messagebox.showinfo("Event Registered", f"Event '{event_name}' has been successfully registered.")
    
    
    def create_first_approval_screen(self):
        """
        Creates the first approval screen for Senior Customer Service (SCS).
        Displays pending approval events with options to approve and lists already approved events.
        """
        self.clear_screen()

        # Label for Pending Approval
        tk.Label(self.root, text="Events Needing Approval").pack()

        # Listbox for Pending Events
        self.pending_events_listbox = tk.Listbox(self.root, width=80, height=10)
        self.pending_events_listbox.pack()

        # Load pending events into the listbox
        pending_events = self.event_manager.get_pending_events()
        
        if not pending_events:
            self.pending_events_listbox.insert(tk.END, "No events pending approval.")
        else:
            for event in pending_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}"
                self.pending_events_listbox.insert(tk.END, event_info)

        # Button to approve/reject selected event
        tk.Button(self.root, text="Approve Selected Event", command=self.approve_selected_event).pack()
        tk.Button(self.root, text="Reject Selected Event", command=self.reject_selected_event).pack()

        # Divider between pending and approved sections
        tk.Label(self.root, text="------------------------").pack()

        # Label for Approved Events
        tk.Label(self.root, text="Approved Events").pack()

        # Listbox for Approved Events
        self.approved_events_listbox = tk.Listbox(self.root, width=80, height=10)
        self.approved_events_listbox.pack()

        # Load approved events into the listbox
        approved_events = self.event_manager.get_approved_events()
        
        if not approved_events:
            self.approved_events_listbox.insert(tk.END, "No approved events.")
        else:
            for event in approved_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}, Status: {event.status}"
                self.approved_events_listbox.insert(tk.END, event_info)

        
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)


    def approve_selected_event(self):
        """ Approves the selected event from the pending events listbox. """
        selected_index = self.pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for approval.")
            return
        
        # Get selected event details
        selected_event_info = self.pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "pending")
        
        if event:
            self.first_approval(event, approved=True)

    def reject_selected_event(self):
        """ Rejects the selected event from the pending events listbox. """
        selected_index = self.pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for rejection.")
            return

        # Get selected event details
        selected_event_info = self.pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "pending")
        
        if event:
            self.first_approval(event, approved=False)

    def find_event_by_info(self, event_info, status):
        """
        Finds the EventRequest object based on displayed event information.
        
        Args:
        - event_info (str): The string info displayed in the listbox.
        - status (str): Indicates if the event is "pending" or "approved".
        
        Returns:
        - EventRequest: The matching event object.
        """
        events = self.event_manager.get_pending_events() if status == "pending" else self.event_manager.get_approved_events()
        for event in events:
            if f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}" in event_info:
                return event
        return None

    def first_approval(self, event, approved):
        """
        Handles the first approval or rejection of an event.
        
        Args:
        - event (EventRequest): The event to approve or reject.
        - approved (bool): Whether the event is approved.
        """
        updated_event = self.event_manager.first_approval(event, approved=approved, reviewer=self.current_user.username)
        
        # Show a message based on approval status
        status = "approved" if approved else "rejected"
        messagebox.showinfo("Approval", f"Event '{event.event_name}' has been {status}.")
        
        # Refresh the approval screen to update the lists
        self.create_first_approval_screen()
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EventOrganizerApp(root)
    root.mainloop()
