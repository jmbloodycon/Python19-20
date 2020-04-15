from flask import Flask, render_template, request
from .status import Status
try:
    from todo_list.task_list import TaskManager
except ModuleNotFoundError:
    from task_list import TaskManager


app = Flask(__name__)
task_list = TaskManager()


@app.route('/')
def index():
    return render_undone_task()


@app.route('/tasks', methods=['post', 'get'])
def tasks():
    if request.method == 'POST':
        done_task_id = request.form.get('id_of_done_task')
        if done_task_id:
            task_list.get_task(done_task_id).mark_done()
            return render_undone_task()

        task_id = request.form.get('new_task_description')
        task_list.add_task(task_id)
        return render_undone_task()

    attrib = request.args.get('status')
    a = request.headers.get('authorization')
    print(a)
    if attrib == Status.UNDONE.value:
        return render_undone_task()
    if attrib == Status.DONE.value:
        return render_done_tasks()
    if attrib == Status.ALL.value:
        return render_all_task()

    return render_undone_task()


def render_done_tasks():
    return render_template('index.html', task_list=task_list.get_completed_tasks())


def render_undone_task():
    return render_template('index.html', task_list=task_list.get_outstanding_tasks())


def render_all_task():
    return render_template('index.html', task_list=task_list.get_all_tasks())


if __name__ == '__main__':
    app.run()
