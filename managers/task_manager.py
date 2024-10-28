import json
from models import Task

class TaskManager:
    def __init__(self, storage_file="tasks.json"):
        self.storage_file = storage_file
        self.tasks = self.load_tasks()  # Load tasks from file

    """------------ SET AND GET FROM JSON FILE ---------------"""

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.storage_file, "w") as f:
            json.dump([self.serialize_task(task) for task in self.tasks], f)
        print("Tasks saved to JSON.")

    def load_tasks(self):
        """Load tasks from a JSON file."""
        try:
            with open(self.storage_file, "r") as f:
                tasks_data = json.load(f)
                print("Tasks loaded from JSON.")
                return [self.deserialize_task(task_data) for task_data in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("No tasks file found or JSON error.")
            return []

        """----------CREATE NEW TASK----------"""

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()  # Save the updated tasks list to the JSON file
        print(f"Task '{task.task_name}' added and saved to JSON.")

    """ ------------  SERIALIZE TASK FOR STORAGE TO JSON ------------ """

    def serialize_task(self, task):
        """Convert a Task object to a serializable dictionary."""
        return {
            "event": task.event,
            "task_name": task.task_name,
            "priority": task.priority,
            "assigned_team": task.assigned_team,
            "status": task.status,
            "created_by": task.created_by
        }

    def deserialize_task(self, data):
        """Convert a dictionary back to a Task object."""
        return Task(
            event=data["event"],
            task_name=data["task_name"],
            priority=data["priority"],
            assigned_team=data["assigned_team"],
            status=data["status"],          # Ensure compatibility with Task constructor
            created_by=data["created_by"]
        )