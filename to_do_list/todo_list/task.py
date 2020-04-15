class Task:
    def __init__(self, description, task_id, done=False):
        self.description = description
        self.done = done
        self.id = task_id

    def mark_done(self):
        self.done = True
