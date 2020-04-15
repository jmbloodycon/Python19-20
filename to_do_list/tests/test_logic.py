import pytest
from todo_list.task import Task
from todo_list.task_list import TaskManager


@pytest.fixture(scope='session')
def todo_list():
    todo_list = TaskManager()
    todo_list.add_task('not dead')
    todo_list.add_task('not dead lvl2')
    todo_list.add_task('alive', True)
    return todo_list


@pytest.fixture(scope='session')
def task():
    return Task('sleep', 1)


def test_todo_add_task(todo_list):
    todo_list.add_task('lol')
    assert len(todo_list.get_outstanding_tasks()) == 3


def test_task_mark_done(todo_list):
    task = todo_list.get_task(2)
    task.mark_done()
    assert task.done


def test_get_task(todo_list):
    task = todo_list.get_task('1')
    assert not task.done


def test_get_all_task(todo_list):
    all_tasks = todo_list.get_all_tasks()
    assert len(all_tasks) == 4


def test_find_task_by_description(todo_list):
    assert len(todo_list.get_tasks_whit_description('not')) == 2


def test_get_done_tasks(todo_list):
    done_tasks = todo_list.get_completed_tasks()
    assert len(done_tasks) == 2


def test_new_task(task):
    assert not task.done


def test_mark_done(task):
    task.mark_done()
    assert task.done
