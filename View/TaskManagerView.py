import customtkinter as ctk
from tkinter import ttk, messagebox

class TaskManagerView(ctk.CTk):
    def __init__(self, controller):
        """Initialize the view and link it to the controller."""
        super().__init__()
        self.controller = controller
        self.title("Task Manager")
        self.geometry("700x500")

        # Styling
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Layout
        self.task_tree = ttk.Treeview(self)
        self.task_tree.heading("#0", text="Tasks", anchor="w")
        self.task_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Form for adding tasks
        self.task_name = ctk.CTkEntry(self, placeholder_text="Task Name")
        self.task_name.pack(pady=5)
        self.task_desc = ctk.CTkEntry(self, placeholder_text="Task Description")
        self.task_desc.pack(pady=5)

        # Dropdown for selecting parent task
        self.parent_task_var = ctk.StringVar()
        self.parent_task_dropdown = ctk.CTkComboBox(self, variable=self.parent_task_var)
        self.parent_task_dropdown.pack(pady=5)

        self.add_task_btn = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_task_btn.pack(pady=5)

        self.add_subtask_btn = ctk.CTkButton(self, text="Add Subtask", command=self.add_subtask)
        self.add_subtask_btn.pack(pady=5)

        self.load_tasks()

    def load_tasks(self):
        """Loads and displays tasks in the TreeView."""
        self.task_tree.delete(*self.task_tree.get_children())
        tasks = self.controller.get_tasks()
        task_map = {}

        # Update the dropdown options
        self.parent_task_dropdown.configure(values=["None"] + [task["name"] for task in tasks])

        for task in tasks:
            if not task["parent_id"]:
                parent_id = self.task_tree.insert("", "end", text=task["name"], values=(task["description"]))
                task_map[task["_id"]] = parent_id
            else:
                parent = task_map.get(task["parent_id"], "")
                task_map[task["_id"]] = self.task_tree.insert(parent, "end", text=task["name"], values=(task["description"]))

    def add_task(self):
        """Handles task creation."""
        name = self.task_name.get()
        desc = self.task_desc.get()

        if name and desc:
            self.controller.add_task(name, desc)
            self.task_name.delete(0, 'end')
            self.task_desc.delete(0, 'end')
        else:
            messagebox.showwarning("Input Error", "Please enter both task name and description")

    def add_subtask(self):
        """Handles subtask creation."""
        name = self.task_name.get()
        desc = self.task_desc.get()
        parent_name = self.parent_task_var.get()

        if parent_name != "None" and name and desc:
            self.controller.add_subtask(parent_name, name, desc)
            self.task_name.delete(0, 'end')
            self.task_desc.delete(0, 'end')
        else:
            messagebox.showwarning("Input Error", "Please select a valid parent task and enter task details")
