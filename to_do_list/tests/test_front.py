import pytest
import todo_list.front as flaskr


@pytest.fixture(scope='session')
def client():
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        yield client


def test_successful_requests(client):
    assert client.get('/').status_code == 200
    assert client.get('/tasks?status=all').status_code == 200
    assert client.get('/tasks?status=done').status_code == 200
    assert client.get('/tasks?status=undone').status_code == 200
    assert client.post('/tasks?new_task=lol').status_code == 200
    assert client.get('/tasks?status=lol').status_code == 200
    assert client.post('/tasks?mark_done=lol').status_code == 200
