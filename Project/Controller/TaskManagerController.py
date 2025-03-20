from Model.TaskModel import TaskModel
from View.TaskManagerView import TaskManagerView

class TaskManagerController:
    def __init__(self):
        """Initialize the controller and link to model and view."""
        self.model = TaskModel()
        self.view = TaskManagerView(self)

    def get_tasks(self):
        """Fetches tasks from the model."""
        return self.model.get_tasks()

    def add_task(self, name, description):
        """Adds a new task."""
        if name and description:
            self.model.create_task(name, description)
            self.view.load_tasks()

    def add_subtask(self, parent_name, name, description):
        """Adds a subtask under a selected parent task."""
        tasks = self.get_tasks()
        parent_task = next((task for task in tasks if task["name"] == parent_name), None)

        if parent_task and name and description:
            self.model.add_subtask(parent_task["_id"], name, description)
            self.view.load_tasks()
