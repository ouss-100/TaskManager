from pymongo import MongoClient

class TaskModel:
    def __init__(self, db_name="TaskManagement", collection_name="tasks"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.tasks_collection = self.db[collection_name]

    def create_task(self, name, description, parent_id=None):
        """Creates a task and adds it to the database."""
        task = {"name": name, "description": description, "parent_id": parent_id, "subtasks": []}
        result = self.tasks_collection.insert_one(task)
        if parent_id:
            self.tasks_collection.update_one({"_id": parent_id}, {"$push": {"subtasks": result.inserted_id}})
        return result.inserted_id

    def add_subtask(self, parent_id, name, description):
        """Adds a subtask to a given parent task."""
        subtask_id = self.create_task(name, description, parent_id)
        self.tasks_collection.update_one({"_id": parent_id}, {"$push": {"subtasks": subtask_id}})
        return subtask_id

    def get_tasks(self):
        """Fetches all tasks from the database."""
        return list(self.tasks_collection.find())
