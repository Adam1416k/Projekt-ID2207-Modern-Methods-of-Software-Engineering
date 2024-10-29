from models import User, Role, EventRequest, Task, RecruitmentRequest, Advert, BudgetRequest
from auth import login, has_access
from managers.event_manager import EventManager
from managers.task_manager import TaskManager
from managers.recruitment_manager import RecruitmentManager
from managers.advert_manager import AdvertManager
from managers.budget_manager import BudgetManager
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class EventOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Organizer")
        self.root.geometry("800x800")
        self.event_manager = EventManager()
        self.task_manager = TaskManager()
        self.recruitment_manager = RecruitmentManager()
        self.advert_manager = AdvertManager()
        self.budget_manager = BudgetManager()
        self.current_user = None
        self.create_login_screen()

    """ ---------FIND AN EVENT BY SELECTING IT IN A VIEW--------- """

    def find_event_by_info(self, event_info, status):
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

        for event in events:
            event_display_info = f"Name: {event.event_name}, Date: {event.date}, Time: {event.time}, Location: {event.location}, Client: {event.client_name}"
            if event_display_info in event_info:
                return event

        return None


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
            self.create_financial_screen()
            # tk.Button(self.root, text="Review Recruitment Requests", command=self.create_financial_review_screen).pack(pady=10) # created a tab for this instead 
        elif has_access(self.current_user, Role.ADMINISTRATIVE_MANAGER):
            self.create_final_approval_screen()
        elif has_access(self.current_user, Role.PRODUCTION_MANAGER):
            self.create_task_screen()
        elif has_access(self.current_user, Role.TEAM_MEMBER):
            self.create_task_review_screen()
        elif has_access(self.current_user, Role.HR_TEAM):  # Updated to Role.HR_TEAM
            self.create_hr_team_screen()
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
        self.clear_screen()
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        # Pending First Approval Tab
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

        # Add approve/reject buttons
        tk.Button(first_approval_tab, text="Approve Selected Event", command=self.approve_selected_event).pack()
        tk.Button(first_approval_tab, text="Reject Selected Event", command=self.reject_selected_event).pack()

        # Approved Events Tab
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

        # Rejected Events Tab
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
                self.rejected_events_listbox.insert(tk.END, event_info)

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



    """ ---------- FINANCIAL REVIEW (FINANCIAL MANAGER) ---------- """

    def create_financial_screen(self):
        """Main screen setup with two tabs for Financial Manager (FM)"""
        self.clear_screen()

        # Create Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        # Financial Comment Tab
        financial_comment_tab = tk.Frame(notebook)
        notebook.add(financial_comment_tab, text="Financial Comments")
        self.setup_financial_comment_tab(financial_comment_tab)

        # Recruitment Review Tab
        recruitment_review_tab = tk.Frame(notebook)
        notebook.add(recruitment_review_tab, text="Recruitment Request Review")
        self.setup_recruitment_review_tab(recruitment_review_tab)

        # Logout Button at the bottom
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    """ ---------- FINANCIAL COMMENT TAB ---------- """

    def setup_financial_comment_tab(self, tab_frame):
        tk.Label(tab_frame, text="Events Needing Financial Comment").pack()

        # Listbox for Events Needing Financial Comment
        self.financial_pending_events_listbox = tk.Listbox(tab_frame, width=80, height=10)
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
        tk.Label(tab_frame, text="Financial Comment").pack()
        self.financial_comment_entry = tk.Entry(tab_frame, width=80)
        self.financial_comment_entry.pack()

        # Button to add comment to the selected event
        tk.Button(tab_frame, text="Add Financial Comment", command=self.add_financial_comment).pack()

        # Divider between pending financial comment and pending final approval sections
        tk.Label(tab_frame, text="------------------------").pack()

        # Label for Events Pending Final Approval
        tk.Label(tab_frame, text="Events Pending Final Approval").pack()

        # Listbox for Events Pending Final Approval
        self.pending_final_approval_listbox = tk.Listbox(tab_frame, width=80, height=10)
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
        tk.Label(tab_frame, text="Selected Event's Financial Comment:").pack()
        self.selected_comment_label = tk.Label(tab_frame, text="", wraplength=500, justify="left")
        self.selected_comment_label.pack()

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
                self.create_financial_manager_screen()  # Refresh screen to move event to next stage
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

    """ ---------- RECRUITMENT REVIEW TAB ---------- """

    def setup_recruitment_review_tab(self, tab_frame):
        tk.Label(tab_frame, text="Pending Recruitment Requests for Financial Review").pack(pady=10)

        # Listbox to display pending requests
        self.request_listbox = tk.Listbox(tab_frame, width=80, height=10)
        self.request_listbox.pack()
        self.load_pending_recruitment_requests()  # Load pending requests

        # Comment entry for financial manager
        tk.Label(tab_frame, text="Financial Manager Comment").pack(pady=5)
        self.fm_comment_entry = tk.Entry(tab_frame, width=80)
        self.fm_comment_entry.pack()

        # Approve and Reject buttons
        tk.Button(tab_frame, text="Approve Request", command=self.approve_selected_request).pack(pady=5)
        tk.Button(tab_frame, text="Reject Request", command=self.reject_selected_request).pack(pady=5)

    def load_pending_recruitment_requests(self):
        self.request_listbox.delete(0, tk.END)
        pending_requests = self.recruitment_manager.get_pending_requests_for_HR()

        if not pending_requests:
            self.request_listbox.insert(tk.END, "No recruitment requests pending review.")
        else:
            for request in pending_requests:
                request_info = f"Position: {request.position}, Hires: {request.num_hires}, Urgency: {request.urgency}, Justification: {request.justification}"
                self.request_listbox.insert(tk.END, request_info)

    def approve_selected_request(self):
        selected_index = self.request_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No recruitment request selected.")
            return

        selected_request_info = self.request_listbox.get(selected_index)
        position = selected_request_info.split(",")[0].split(":")[1].strip()  # Extract position

        request = next((req for req in self.recruitment_manager.requests if req.position == position), None)
        if not request:
            messagebox.showerror("Request Not Found", "The selected recruitment request could not be found.")
            return

        comment = self.fm_comment_entry.get().strip()
        if not comment:
            messagebox.showwarning("Empty Comment", "Please enter a comment before approving.")
            return

        self.recruitment_manager.approve_request(request, comment)
        messagebox.showinfo("Request Approved", f"Recruitment request for '{position}' approved.")
        self.load_pending_recruitment_requests()  # Refresh list

    def reject_selected_request(self):
        selected_index = self.request_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No recruitment request selected.")
            return

        selected_request_info = self.request_listbox.get(selected_index)
        position = selected_request_info.split(",")[0].split(":")[1].strip()  # Extract position

        request = next((req for req in self.recruitment_manager.requests if req.position == position), None)
        if not request:
            messagebox.showerror("Request Not Found", "The selected recruitment request could not be found.")
            return

        comment = self.fm_comment_entry.get().strip()
        if not comment:
            messagebox.showwarning("Empty Comment", "Please enter a comment before rejecting.")
            return

        self.recruitment_manager.reject_request(request, comment)
        messagebox.showinfo("Request Rejected", f"Recruitment request for '{position}' rejected.")
        self.load_pending_recruitment_requests()  # Refresh list

    """ ---------- CLEAR SCREEN HELPER ---------- """

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    

    """ ---------- TASK CREATION (PRODUCTION MANAGER VIEW) ---------- """

    def create_task_screen(self):
        """Main screen setup with three tabs for Production Manager (PM)"""
        self.clear_screen()

        # Create Notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        # Task Creation Tab
        task_creation_tab = tk.Frame(notebook)
        notebook.add(task_creation_tab, text="Task Creation")
        self.setup_task_creation_tab(task_creation_tab)

        # Reviewed Tasks Tab
        reviewed_tasks_tab = tk.Frame(notebook)
        notebook.add(reviewed_tasks_tab, text="Reviewed Tasks")
        self.setup_reviewed_tasks_tab(reviewed_tasks_tab)

        # Recruitment Request Tab
        recruitment_request_tab = tk.Frame(notebook)
        notebook.add(recruitment_request_tab, text="Recruitment Requests")
        self.setup_recruitment_request_tab(recruitment_request_tab)

        budget_request_tab = tk.Frame(notebook)
        notebook.add(budget_request_tab, text="Budget Requests")
        self.setup_budget_request_tab(budget_request_tab)

        # Logout Button at the bottom
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    """ ---------- TASK CREATION TAB ---------- """

    def setup_task_creation_tab(self, tab_frame):
        tk.Label(tab_frame, text="Select an Approved Event").pack()

        # Load approved events
        approved_events = self.event_manager.get_approved_events_for_final_approval()
        self.approved_events_map = {f"{event.event_name} - {event.date}": event for event in approved_events}

        # Event selection dropdown
        self.selected_event_var = tk.StringVar(tab_frame)
        if approved_events:
            first_event_name = list(self.approved_events_map.keys())[0]
            self.selected_event_var.set(first_event_name)
            self.selected_event = self.approved_events_map[first_event_name]
            event_options = list(self.approved_events_map.keys())
        else:
            self.selected_event_var.set("No Approved Events Available")
            self.selected_event = None
            event_options = ["No Approved Events Available"]

        # Dropdown menu for events
        self.event_dropdown = tk.OptionMenu(tab_frame, self.selected_event_var, *event_options, command=self.update_selected_event)
        self.event_dropdown.pack()

        # Task Name Entry
        tk.Label(tab_frame, text="Task Name").pack()
        self.task_name_entry = tk.Entry(tab_frame)
        self.task_name_entry.pack()

        # Task Priority Dropdown
        tk.Label(tab_frame, text="Select Task Priority").pack()
        self.priority_var = tk.StringVar(tab_frame)
        self.priority_var.set("Medium")
        tk.OptionMenu(tab_frame, self.priority_var, "High", "Medium", "Low").pack()

        # Assigned Team Dropdown
        tk.Label(tab_frame, text="Select Assigned Team").pack()
        team_options = ["Marketing", "Production", "Support", "Sales"]
        self.assigned_team_var = tk.StringVar(tab_frame)
        self.assigned_team_var.set(team_options[0])
        tk.OptionMenu(tab_frame, self.assigned_team_var, *team_options).pack()


        # Create Task Button
        tk.Button(tab_frame, text="Create Task", command=self.create_task_for_event).pack(pady=10)

    def update_selected_event(self, selected_event_name):
        self.selected_event = self.approved_events_map.get(selected_event_name)

    def create_task_for_event(self):
        if not self.selected_event:
            messagebox.showwarning("No Event Selected", "Please select an approved event to create a task.")
            return

        task_name = self.task_name_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Empty Task Name", "Please enter a name for the task.")
            return
        priority = self.priority_var.get()
        assigned_team = self.assigned_team_var.get()
        created_by = self.current_user.username

        task = Task(
            event=self.selected_event.event_name,
            task_name=task_name,
            priority=priority,
            assigned_team=assigned_team,
            created_by=created_by
        )
        self.task_manager.add_task(task)
        messagebox.showinfo("Task Created", f"Task '{task_name}' created for event '{self.selected_event.event_name}' "
                                            f"with priority '{priority}' and assigned team '{assigned_team}'.")
        self.task_name_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.assigned_team_var.set("Marketing")

    """ ---------- REVIEWED TASKS TAB ---------- """

    def setup_reviewed_tasks_tab(self, tab_frame):
        tk.Label(tab_frame, text="Reviewed Tasks").pack(pady=10)
        self.reviewed_tasks_listbox = tk.Listbox(tab_frame, width=80, height=10)
        self.reviewed_tasks_listbox.pack()
        self.load_reviewed_tasks()  # Load tasks with "Reviewed" status

    def load_reviewed_tasks(self):
        reviewed_tasks = self.task_manager.get_reviewed_tasks()
        self.reviewed_tasks_listbox.delete(0, tk.END)
        if not reviewed_tasks:
            self.reviewed_tasks_listbox.insert(tk.END, "No reviewed tasks available.")
        else:
            for task in reviewed_tasks:
                task_info = f"Task: {task.task_name}, Event: {task.event}, Priority: {task.priority}, Comments: {', '.join(task.comments)}"
                self.reviewed_tasks_listbox.insert(tk.END, task_info)

    """ ---------- RECRUITMENT REQUEST TAB ---------- """

    def setup_recruitment_request_tab(self, tab_frame):
        tk.Label(tab_frame, text="Recruitment Request Form").pack(pady=10)

        # Position Entry
        tk.Label(tab_frame, text="Position").pack()
        self.position_entry = tk.Entry(tab_frame)
        self.position_entry.pack()

        # Number of Hires Entry
        tk.Label(tab_frame, text="Number of Hires").pack()
        self.num_hires_entry = tk.Entry(tab_frame)
        self.num_hires_entry.pack()

        # Urgency Dropdown
        tk.Label(tab_frame, text="Urgency").pack()
        self.urgency_var = tk.StringVar(tab_frame)
        self.urgency_var.set("Medium")
        tk.OptionMenu(tab_frame, self.urgency_var, "High", "Medium", "Low").pack()

        # Justification Entry
        tk.Label(tab_frame, text="Justification").pack()
        self.justification_entry = tk.Entry(tab_frame, width=50)
        self.justification_entry.pack()

        # Submit Button
        tk.Button(tab_frame, text="Submit Recruitment Request", command=self.submit_recruitment_request).pack(pady=20)

    def submit_recruitment_request(self):
        position = self.position_entry.get().strip()
        num_hires = self.num_hires_entry.get().strip()
        urgency = self.urgency_var.get()
        justification = self.justification_entry.get().strip()

        if not position or not num_hires.isdigit() or not justification:
            messagebox.showerror("Invalid Input", "Please enter valid information for all fields.")
            return

        request = RecruitmentRequest(
            position=position,
            num_hires=int(num_hires),
            urgency=urgency,
            justification=justification,
            submitted_by=self.current_user.username
        )
        self.recruitment_manager.add_request(request)
        messagebox.showinfo("Request Submitted", "Your recruitment request has been submitted to HR.")
        self.position_entry.delete(0, tk.END)
        self.num_hires_entry.delete(0, tk.END)
        self.justification_entry.delete(0, tk.END)
        self.urgency_var.set("Medium")


        # ----------- Budget Request Tab-------------
    


    def setup_budget_request_tab(self, tab_frame):
        """Sets up the budget request tab for creating budget requests for tasks."""
        tk.Label(tab_frame, text="Select a Task for Budget Request").pack(pady=5)

        # Load tasks
        tasks = self.task_manager.load_tasks()  # Assuming load_tasks() returns a list of tasks
        self.task_map = {f"{task.task_name} ({task.event})": task for task in tasks}

        # Populate the task dropdown
        task_options = list(self.task_map.keys())
        self.selected_task_var = tk.StringVar(tab_frame)
        if task_options:
            self.selected_task_var.set(task_options[0])  # Default to the first task
        else:
            self.selected_task_var.set("No tasks available")

        tk.OptionMenu(tab_frame, self.selected_task_var, *task_options).pack()

        # Budget Amount Entry
        tk.Label(tab_frame, text="Requested Budget Amount").pack(pady=5)
        self.budget_amount_entry = tk.Entry(tab_frame)
        self.budget_amount_entry.pack()

        # Submit Budget Request Button
        tk.Button(tab_frame, text="Submit Budget Request", command=self.submit_budget_request).pack(pady=10)

    def submit_budget_request(self):
        """Handles the submission of a budget request for a selected task."""
        # Validate task selection
        selected_task_name = self.selected_task_var.get()
        if selected_task_name == "No tasks available" or selected_task_name not in self.task_map:
            messagebox.showwarning("Task Selection Error", "Please select a valid task.")
            return

        # Validate budget amount
        budget_amount_str = self.budget_amount_entry.get().strip()
        if not budget_amount_str.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid numeric budget amount.")
            return
        budget_amount = int(budget_amount_str)

        # Get the selected task object
        selected_task = self.task_map[selected_task_name]

        # Create a BudgetRequest object
        budget_request = BudgetRequest(
            task_name=selected_task.task_name,
            requested_by=self.current_user.username,  # Set the requesting user
            amount=budget_amount
        )

        # Add the budget request to the manager and save to JSON
        self.budget_manager.add_request(budget_request)

        # Confirmation message and clear input
        messagebox.showinfo("Budget Request Submitted", f"Budget request for '{selected_task.task_name}' submitted.")
        self.budget_amount_entry.delete(0, tk.END)  # Clear the budget amount entry


    """ ---------- TASK REVIEW (SUB TEAM VIEW) ---------- """

    def create_task_review_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Assigned Tasks for Review").pack()

        # Listbox for displaying assigned tasks
        self.task_listbox = tk.Listbox(self.root, width=80, height=10)
        self.task_listbox.pack()
        self.load_assigned_tasks()  # Load tasks for the logged-in team

        # Text entry for review comment
        tk.Label(self.root, text="Add Review Comment").pack()
        self.review_comment_entry = tk.Entry(self.root, width=80)
        self.review_comment_entry.pack()

        # Button to submit the review comment
        self.submit_comment_button = tk.Button(self.root, text="Submit Comment", command=self.add_task_comment)
        self.submit_comment_button.pack(pady=10)

        # Bind selection to check if task can be commented
        self.task_listbox.bind("<<ListboxSelect>>", self.check_task_review_status)

        # Logout Button
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def check_task_review_status(self, event):
        # Disable comment entry if the selected task is already reviewed
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return

        # Get selected task details
        selected_task_info = self.task_listbox.get(selected_index)
        task_name = selected_task_info.split(",")[0].split(":")[1].strip()

        # Find the task object
        task = next((task for task in self.task_manager.tasks if task.task_name == task_name), None)

        # Disable comment input if already reviewed
        if task and task.status == "Reviewed":
            self.review_comment_entry.config(state="disabled")
            self.submit_comment_button.config(state="disabled")
        else:
            self.review_comment_entry.config(state="normal")
            self.submit_comment_button.config(state="normal")

    def load_assigned_tasks(self):
        # Clear existing items in the listbox
        self.task_listbox.delete(0, tk.END)

        # Retrieve tasks assigned to the current team
        assigned_team = "Marketing"  # Assume the current team is Marketing; adjust based on team logic
        assigned_tasks = [task for task in self.task_manager.tasks if task.assigned_team == assigned_team]

        if not assigned_tasks:
            self.task_listbox.insert(tk.END, "No tasks assigned to your team.")
        else:
            for task in assigned_tasks:
                status_text = "(Reviewed)" if task.status == "Reviewed" else "(Pending Review)"
                task_info = f"Task: {task.task_name}, Event: {task.event}, Priority: {task.priority} {status_text}"
                self.task_listbox.insert(tk.END, task_info)

    def add_task_comment(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No task selected for comment.")
            return

        # Get selected task details
        selected_task_info = self.task_listbox.get(selected_index)
        task_name = selected_task_info.split(",")[0].split(":")[1].strip()  # Extract task name from display

        # Find the task object
        task = next((task for task in self.task_manager.tasks if task.task_name == task_name), None)
        if not task:
            messagebox.showerror("Task Not Found", "The selected task could not be found.")
            return

        # Check if the task has already been reviewed
        if task.status == "Reviewed":
            messagebox.showinfo("Task Already Reviewed", f"Task '{task.task_name}' has already been reviewed.")
            return

        # Get comment from entry box
        comment = self.review_comment_entry.get().strip()
        if not comment:
            messagebox.showwarning("Empty Comment", "Please enter a review comment before submitting.")
            return

        # Append comment to the task and mark as reviewed
        task.status = "Reviewed"  # Update status to reviewed
        task.comments.append(comment)

        # Save tasks to JSON
        self.task_manager.save_tasks()

        # Confirm submission and clear input
        messagebox.showinfo("Comment Added", f"Review comment added to task '{task.task_name}'.")
        self.review_comment_entry.delete(0, tk.END)  # Clear the comment entry
        self.load_assigned_tasks()  # Refresh the task list

    def load_reviewed_tasks(self):
        # Clear existing items in the listbox
        self.reviewed_tasks_listbox.delete(0, tk.END)

        # Filter for tasks with status "Reviewed"
        reviewed_tasks = [task for task in self.task_manager.tasks if task.status == "Reviewed"]

        if not reviewed_tasks:
            self.reviewed_tasks_listbox.insert(tk.END, "No reviewed tasks available.")
        else:
            for task in reviewed_tasks:
                task_info = f"Task: {task.task_name}, Event: {task.event}, Priority: {task.priority}, Comments: {', '.join(task.comments)}"
                self.reviewed_tasks_listbox.insert(tk.END, task_info)






    """ ---------- RECRUITMENT VIEW (HR TEAM VIEW) ---------- """

    def create_hr_team_screen(self):
        """Sets up the HR team interface with two tabs: Recruitment Review and Job Advertisement."""
        self.clear_screen()

        # Create Notebook for Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        # Tab 1: Review Recruitment Requests
        review_tab = tk.Frame(notebook)
        notebook.add(review_tab, text="Review Recruitment Requests")
        self.setup_recruitment_review_tab(review_tab)

        # Tab 2: Create Job Advertisement
        advertisement_tab = tk.Frame(notebook)
        notebook.add(advertisement_tab, text="Create Job Advertisement")
        self.setup_advertisement_tab(advertisement_tab)

        # Logout Button (appears at the bottom of both tabs)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def setup_recruitment_review_tab(self, tab):
        """Sets up the recruitment request review tab for HR."""
        tk.Label(tab, text="Pending Recruitment Requests for HR Review").pack(pady=10)

        # Listbox to display pending requests
        self.request_listbox = tk.Listbox(tab, width=80, height=10)
        self.request_listbox.pack()
        self.load_pending_recruitment_requests()  # Load pending requests

        # Comment entry for HR team
        tk.Label(tab, text="HR Comment").pack(pady=5)
        self.hr_comment_entry = tk.Entry(tab, width=80)
        self.hr_comment_entry.pack()

        # Approve and Reject buttons
        tk.Button(tab, text="Approve Request", command=self.approve_selected_request_by_hr).pack(pady=5)
        tk.Button(tab, text="Reject Request", command=self.reject_selected_request_by_hr).pack(pady=5)

    def approve_selected_request_by_hr(self):
        """Approves the selected recruitment request with an HR comment."""
        selected_index = self.request_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No recruitment request selected.")
            return

        selected_request_info = self.request_listbox.get(selected_index)
        position = selected_request_info.split(",")[0].split(":")[1].strip()

        request = next((req for req in self.recruitment_manager.requests if req.position == position), None)
        if not request:
            messagebox.showerror("Request Not Found", "The selected recruitment request could not be found.")
            return

        comment = self.hr_comment_entry.get().strip()
        if not comment:
            messagebox.showwarning("Empty Comment", "Please enter a comment before approving.")
            return

        self.recruitment_manager.approve_request_by_hr(request, comment)
        messagebox.showinfo("Request Approved", f"Recruitment request for '{position}' approved by HR.")
        self.load_pending_recruitment_requests()  # Refresh list

    def reject_selected_request_by_hr(self):
        """Rejects the selected recruitment request with an HR comment."""
        selected_index = self.request_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No recruitment request selected.")
            return

        selected_request_info = self.request_listbox.get(selected_index)
        position = selected_request_info.split(",")[0].split(":")[1].strip()

        request = next((req for req in self.recruitment_manager.requests if req.position == position), None)
        if not request:
            messagebox.showerror("Request Not Found", "The selected recruitment request could not be found.")
            return

        comment = self.hr_comment_entry.get().strip()
        if not comment:
            messagebox.showwarning("Empty Comment", "Please enter a comment before rejecting.")
            return

        self.recruitment_manager.reject_request_by_hr(request, comment)
        messagebox.showinfo("Request Rejected", f"Recruitment request for '{position}' rejected by HR.")
        self.load_pending_recruitment_requests()  # Refresh list

    def setup_advertisement_tab(self, tab):
        """Sets up the job advertisement creation tab."""
        tk.Label(tab, text="Create Job Advertisement").pack(pady=10)

        # Position Entry
        tk.Label(tab, text="Position").pack()
        self.position_entry = tk.Entry(tab)
        self.position_entry.pack()

        # Start Date Entry
        tk.Label(tab, text="Start Date (YYYY-MM-DD)").pack()
        self.start_date_entry = tk.Entry(tab)
        self.start_date_entry.pack()

        # Coverage Dropdown (Full-time or Part-time)
        tk.Label(tab, text="Job Coverage").pack()
        self.coverage_var = tk.StringVar(tab)
        self.coverage_var.set("Full-time")
        tk.OptionMenu(tab, self.coverage_var, "Full-time", "Part-time").pack()

        # Experience Entry
        tk.Label(tab, text="Experience (Years)").pack()
        self.experience_entry = tk.Entry(tab)
        self.experience_entry.pack()

        # Submit Button
        tk.Button(tab, text="Create Advertisement", command=self.submit_job_advertisement).pack(pady=20)

    def submit_job_advertisement(self):
        """Creates and submits a job advertisement."""
        position = self.position_entry.get().strip()
        start_date_str = self.start_date_entry.get().strip()
        coverage = self.coverage_var.get()
        experience = self.experience_entry.get().strip()

        # Validate inputs
        if not position or not experience.isdigit():
            messagebox.showerror("Invalid Input", "Please provide valid information for all fields.")
            return

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid start date (YYYY-MM-DD).")
            return

        # Create an Advert object and add to the manager
        advert = Advert(position=position, start_date=start_date, coverage=coverage, experience=int(experience), hr_comment=[])
        self.advert_manager.add_advert(advert)
        messagebox.showinfo("Advertisement Created", f"Job advertisement for '{position}' created.")

        # Clear form inputs
        self.position_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.coverage_var.set("Full-time")
        self.experience_entry.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = EventOrganizerApp(root)
    root.mainloop()