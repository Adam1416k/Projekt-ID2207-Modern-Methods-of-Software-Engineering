# gui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import * # not working, why?? 
from tkinter import ttk 
from datetime import datetime, date, time
from models import EventRequest, Role, Task
from managers.event_manager import EventManager
from auth import login, has_access

class EventOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Organizer")
        self.event_manager = EventManager()
        self.current_user = None
        self.create_login_screen()

    """ ---------FIND AN EVENT BY SELECTING IT IN A VIEW--------- """

    def find_event_by_info(self, event_info, status):

        # Retrieve the correct list of events based on status
        if status == "Pending First Approval":
            events = self.event_manager.get_pending_events_for_first_approval()
        elif status == "Pending Financial Assessment":
            events = self.event_manager.get_pending_events_for_fin_com()
        elif status == "Pending Final Approval":
            events = self.event_manager.get_assessed_events_for_fin_com()
        elif status == "Approved":
            events = self.event_manager.get_approved_events_for_final_approval()
        else:
            events = []

        # Iterate through the events and find the one matching the event_info string
        for event in events:
            event_display_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}"
            if event_display_info in event_info:
                return event

        return None  # Return None if no matching event is found


    """----------  LOGIN + LOGOUT STORY ---------- """

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
        elif has_access(self.current_user, Role.FINANCIAL_MANAGER):
            self.create_financial_comment_screen()  
        elif has_access(self.current_user, Role.ADMINISTRATIVE_MANAGER):
            self.create_final_approval_screen()
        elif has_access(self.current_user, Role.PRODUCTION_MANAGER):
            self.create_task_screen()
        else:
            messagebox.showerror("Access Denied", "You do not have access to any screens.")

    def logout(self):
        """Logs out the current user and returns to the login screen."""
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out.")
        self.create_login_screen()  # Redirect to login screen




    """ ---------- EVENT CREATION STORY (CS VIEW) ---------- """

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
    
    

    """ ---------- FIRST APPROVAL STORY (SCS VIEW)---------- """

    def create_first_approval_screen(self):
        """
        Creates the tabbed interface for Senior Customer Service (SCS).
        Includes tabs for:
        1. Events Needing First Approval
        2. All Final Approved Events
        """
        self.clear_screen()

        # Create Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        # First tab: Events Needing First Approval
        first_approval_tab = tk.Frame(notebook)
        notebook.add(first_approval_tab, text="Pending First Approval")

        tk.Label(first_approval_tab, text="Events Needing First Approval").pack()

        self.first_approval_pending_events_listbox = tk.Listbox(first_approval_tab, width=80, height=10)
        self.first_approval_pending_events_listbox.pack()

        pending_events = self.event_manager.get_pending_events_for_first_approval()
        
        if not pending_events:
            self.first_approval_pending_events_listbox.insert(tk.END, "No events pending approval.")
        else:
            for event in pending_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}"
                self.first_approval_pending_events_listbox.insert(tk.END, event_info)

        tk.Button(first_approval_tab, text="Approve Selected Event", command=self.approve_selected_event).pack()
        tk.Button(first_approval_tab, text="Reject Selected Event", command=self.reject_selected_event).pack()

            # Section for events pending financial comment
        Label(first_approval_tab, text="Events Awaiting Financial Comment").pack()

        self.pending_financial_comment_listbox = Listbox(first_approval_tab, width=80, height=10)
        self.pending_financial_comment_listbox.pack()

        approved_for_financial = self.event_manager.get_approved_events_for_first_approval()
        
        if not approved_for_financial:
            self.pending_financial_comment_listbox.insert(END, "No events awaiting financial comment.")
        else:
            for event in approved_for_financial:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}, Status: {event.status}"
                self.pending_financial_comment_listbox.insert(END, event_info)


        # Second tab: All Final Approved Events
        final_approved_tab = tk.Frame(notebook)
        notebook.add(final_approved_tab, text="Final Approved Events")

        tk.Label(final_approved_tab, text="All Final Approved Events").pack()

        self.final_approved_events_listbox = tk.Listbox(final_approved_tab, width=80, height=10)
        self.final_approved_events_listbox.pack()

        final_approved_events = self.event_manager.get_approved_events_for_final_approval()
        
        if not final_approved_events:
            self.final_approved_events_listbox.insert(tk.END, "No final approved events.")
        else:
            for event in final_approved_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}, Status: {event.status}"
                self.final_approved_events_listbox.insert(tk.END, event_info)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

        
        # Third tab: All Rejected Events
        rejected_tab = tk.Frame(notebook)
        notebook.add(rejected_tab, text="Rejected Events")

        tk.Label(rejected_tab, text="All Rejected Events").pack()

        self.rejected_events_listbox = tk.Listbox(rejected_tab, width=80, height=10)
        self.rejected_events_listbox.pack()

        rejected_events = self.event_manager.get_rejected_events()
        
        if not rejected_events:
            self.rejected_events_listbox.insert(tk.END, "No rejected events.")
        else:
            for event in rejected_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}, Status: {event.status}"
                self.rejected_events.insert(tk.END, event_info)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def approve_selected_event(self):
        """ Approves the selected event from the pending events listbox. """
        selected_index = self.first_approval_pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for approval.")
            return
        
        # Get selected event details
        selected_event_info = self.first_approval_pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "Pending First Approval")
        
        if event:
            self.first_approval(event, approved=True)

    def reject_selected_event(self):
        """ Rejects the selected event from the pending events listbox. """
        selected_index = self.first_approval_pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for rejection.")
            return

        # Get selected event details
        selected_event_info = self.first_approval_pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "Pending First Approval")
        
        if event:
            self.first_approval(event, approved=False)

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


    """ ---------- FINANCIAL COMMENTING STORY (FINANCIAL MANAGER VIEW) ---------- """

    def create_financial_comment_screen(self):
        """
        Creates the financial commenting screen for the Financial Manager.
        Displays events that require a financial comment and shows a list of events
        that are pending final approval along with their comments when selected.
        """
        self.clear_screen()

        # Label for Events Needing Financial Comment
        tk.Label(self.root, text="Events Needing Financial Comment").pack()

        # Listbox for Events Needing Financial Comment
        self.financial_pending_events_listbox = tk.Listbox(self.root, width=80, height=10)
        self.financial_pending_events_listbox.pack()

        # Load pending financial assessment events into the listbox
        pending_events = self.event_manager.get_pending_events_for_fin_com()
        
        if not pending_events:
            self.financial_pending_events_listbox.insert(tk.END, "No events pending financial comment.")
        else:
            for event in pending_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}"
                self.financial_pending_events_listbox.insert(tk.END, event_info)

        # Text entry for financial comment
        tk.Label(self.root, text="Financial Comment").pack()
        self.financial_comment_entry = tk.Entry(self.root, width=80)
        self.financial_comment_entry.pack()

        # Button to add comment to the selected event
        tk.Button(self.root, text="Add Financial Comment", command=self.add_financial_comment).pack()

        # Divider between pending financial comment and pending final approval sections
        tk.Label(self.root, text="------------------------").pack()

        # Label for Events Pending Final Approval
        tk.Label(self.root, text="Events Pending Final Approval").pack()

        # Listbox for Events Pending Final Approval
        self.pending_final_approval_listbox = tk.Listbox(self.root, width=80, height=10)
        self.pending_final_approval_listbox.pack()
        self.pending_final_approval_listbox.bind("<<ListboxSelect>>", self.display_financial_comment)

        # Load events pending final approval into the listbox
        pending_final_events = self.event_manager.get_pending_events_for_final_approval()
        
        if not pending_final_events:
            self.pending_final_approval_listbox.insert(tk.END, "No events pending final approval.")
        else:
            for event in pending_final_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}, Status: {event.status}"
                self.pending_final_approval_listbox.insert(tk.END, event_info)

        # Label to display selected event's financial comment
        tk.Label(self.root, text="Selected Event's Financial Comment:").pack()
        self.selected_comment_label = tk.Label(self.root, text="", wraplength=500, justify="left")
        self.selected_comment_label.pack()

        # Logout button
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def add_financial_comment(self):
        """Adds a financial comment to the selected event."""
        selected_index = self.financial_pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for financial comment.")
            return

        # Get selected event details
        selected_event_info = self.financial_pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "Pending Financial Assessment")
        
        if event:
            # Get the comment from the entry box
            comment = self.financial_comment_entry.get()
            if comment.strip():
                # Add comment to event and save
                self.event_manager.add_financial_comment(event, comment, reviewer=self.current_user.username)
                messagebox.showinfo("Comment Added", f"Financial comment added by {self.current_user.username}.")
                self.create_financial_comment_screen()  # Refresh screen to move event to next stage
            else:
                messagebox.showwarning("Empty Comment", "Please enter a financial comment before submitting.")

    def display_financial_comment(self, event):
        """Displays the financial comment of the selected event from pending final approval list."""
        selected_index = self.pending_final_approval_listbox.curselection()
        if not selected_index:
            self.selected_comment_label.config(text="No comment available.")
            return

        # Get selected event details
        selected_event_info = self.pending_final_approval_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "Pending Final Approval")

        if event:
            # Display the financial comment in the label
            financial_comment = event.comments.get("financial", "No comment available.")
            self.selected_comment_label.config(text=financial_comment)
        else:
            self.selected_comment_label.config(text="No comment available.")




    """ ---------- FINAL APPROVAL STORY (ADMINISTRATIVE MANAGER VIEW) ---------- """

    def create_final_approval_screen(self):
        """
        Creates the final approval screen for Administrative Manager.
        Displays events that have been financially commented and allows final approval.
        """
        self.clear_screen()

        # Label for Pending Final Approval
        tk.Label(self.root, text="Events Pending Final Approval").pack()

        # Listbox for Pending Final Approval
        self.final_approval_pending_events_listbox = tk.Listbox(self.root, width=80, height=10)
        self.final_approval_pending_events_listbox.pack()

        # Load pending final approval events into the listbox
        pending_events = self.event_manager.get_pending_events_for_final_approval()
        
        if not pending_events:
            self.final_approval_pending_events_listbox.insert(tk.END, "No events pending final approval.")
        else:
            for event in pending_events:
                event_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}"
                self.final_approval_pending_events_listbox.insert(tk.END, event_info)

        # Button to approve/reject selected event
        tk.Button(self.root, text="Approve Selected Event", command=self.final_approve_selected_event).pack()
        tk.Button(self.root, text="Reject Selected Event", command=self.final_reject_selected_event).pack()

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def final_approve_selected_event(self):
        """Approves the selected event from the pending final approval listbox."""
        selected_index = self.final_approval_pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for final approval.")
            return

        # Get selected event details
        selected_event_info = self.final_approval_pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "Pending Final Approval")
        
        if event:
            self.event_manager.final_approval(event, approved=True, reviewer=self.current_user.username)
            messagebox.showinfo("Final Approval", f"Event '{event.event_name}' has been finally approved.")
            self.create_final_approval_screen()  # Refresh screen

    def final_reject_selected_event(self):
        """Rejects the selected event from the pending final approval listbox."""
        selected_index = self.final_approval_pending_events_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No event selected for rejection.")
            return

        # Get selected event details
        selected_event_info = self.final_approval_pending_events_listbox.get(selected_index)
        event = self.find_event_by_info(selected_event_info, "Pending Final Approval")
        
        if event:
            self.event_manager.final_approval(event, approved=False, reviewer=self.current_user.username)
            messagebox.showinfo("Final Rejection", f"Event '{event.event_name}' has been rejected.")
            self.create_final_approval_screen()  # Refresh screen

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    

    """ ---------- TASK CREATION (PRODUCTION MANAGER VIEW) ---------- """


    def create_task_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Select an Approved Event").pack()

        # Retrieve approved events and create a dictionary for mapping
        approved_events = self.event_manager.get_approved_events_for_final_approval()
        self.approved_events_map = {f"{event.event_name} - {event.date}": event for event in approved_events}

        # Create a dropdown with approved events
        self.selected_event_var = tk.StringVar(self.root)
        if approved_events:
            first_event_name = list(self.approved_events_map.keys())[0]
            self.selected_event_var.set(first_event_name)
            self.selected_event = self.approved_events_map[first_event_name]  # Set the default selected event
        else:
            self.selected_event_var.set("No Approved Events Available")
            self.selected_event = None

        self.event_dropdown = tk.OptionMenu(
            self.root, self.selected_event_var, *self.approved_events_map.keys(), command=self.update_selected_event
        )
        self.event_dropdown.pack()

        # Task name entry
        tk.Label(self.root, text="Task Name").pack()
        self.task_name_entry = tk.Entry(self.root)
        self.task_name_entry.pack()

        # Task priority dropdown
        tk.Label(self.root, text="Select Task Priority").pack()
        self.priority_var = tk.StringVar(self.root)
        self.priority_var.set("Medium")
        self.priority_dropdown = tk.OptionMenu(self.root, self.priority_var, "High", "Medium", "Low")
        self.priority_dropdown.pack()

        # Assigned team dropdown
        tk.Label(self.root, text="Select Assigned Team").pack()
        team_options = ["Marketing", "Production", "Support", "Sales"]
        self.assigned_team_var = tk.StringVar(self.root)
        self.assigned_team_var.set(team_options[0])
        self.team_dropdown = tk.OptionMenu(self.root, self.assigned_team_var, *team_options) # TMP team options
        self.team_dropdown.pack()

        # Create Task button
        tk.Button(self.root, text="Create Task", command=self.create_task_for_event).pack(pady=10)

    def update_selected_event(self, selected_event_name):
        """Updates self.selected_event based on the dropdown selection."""
        self.selected_event = self.approved_events_map.get(selected_event_name)


    def create_task_for_event(self):
        if not hasattr(self, 'selected_event') or self.selected_event is None:
            messagebox.showwarning("No Event Selected", "Please select an approved event to create a task.")
            return

        # Retrieve the task name, priority level, and assigned team
        task_name = self.task_name_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Empty Task Name", "Please enter a name for the task.")
            return
        
        priority = self.priority_var.get()
        assigned_team = self.assigned_team_var.get()
        created_by = self.current_user.username

        # Create the Task object with the required attributes
        task = Task(
            event=self.selected_event.event_name,  # Use the name of the selected event as the event reference ?? OBS OBS kolla om detta är bästa sätt
            task_name=task_name,
            priority=priority,
            assigned_team=assigned_team,
            created_by=created_by
        )

        self.task_manager.add_task(task)
        
        # Show a confirmation message
        messagebox.showinfo("Task Created", f"Task '{task_name}' created for event '{self.selected_event.event_name}' "
                                            f"with priority '{priority}' and assigned team '{assigned_team}'.")

        self.task_name_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.assigned_team_var.set("Marketing")


if __name__ == "__main__":
    root = tk.Tk()
    app = EventOrganizerApp(root)
    root.mainloop()
