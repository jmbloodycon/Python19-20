try:
    from todo_list.task import Task
except ModuleNotFoundError:
    from task import Task


class TaskManager:
    def __init__(self):
        self._all_tasks = {}
        self.task_count = 0

    def add_task(self, description, done=False):
        self.task_count += 1
        self._all_tasks[self.task_count] = Task(description, self.task_count, done)

    def get_task(self, task_id):
        return self._all_tasks[int(task_id)]

    def get_tasks_whit_description(self, description):
        task_list = []
        for task in self._all_tasks.values():
            position = task.description.find(description)
            if position > -1:
                task_list.append(task)

        return task_list

    def get_outstanding_tasks(self):
        res_list = []
        for task in self._all_tasks.values():
            if not task.done:
                res_list.append(task)
        return res_list

    def get_completed_tasks(self):
        res_list = []
        for task in self._all_tasks.values():
            if task.done:
                res_list.append(task)
        return res_list

    def get_all_tasks(self):
        return self._all_tasks.values()
