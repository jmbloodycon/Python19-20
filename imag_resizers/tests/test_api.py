import pytest
import image_resizer.api as flaskr
from flask import json
from http import HTTPStatus
from base64 import b64encode


@pytest.fixture(scope='session')
def client():
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        yield client


def test_new_task_bad_request(client):
    massage = {'username': 'lol'}
    data = client.post('/task', data=json.dumps(massage), content_type='application/json')
    assert data.status_code == HTTPStatus.BAD_REQUEST


def test_get_image_bad_request(client):
    massage = {'user': 'lol'}
    data = client.get('/image/2', data=json.dumps(massage), content_type='application/json')
    assert data.status_code == HTTPStatus.BAD_REQUEST

#
# def test_get_status_bad_request(client):
#     massage = {'user': 'lol'}
#     data = client.get('/task/2', data=json.dumps(massage), content_type='application/json')
#     assert data.status_code == HTTPStatus.NOT_FOUND
#
#
# def test_add_task(client):
#     with open('tests/1.jpg', 'rb') as f:
#         image = f.read()
#     byte_image = b64encode(image)
#     massage = {'image': byte_image}
#     data = client.post('/task', data=json.dumps(massage), content_type='application/json')
#     assert data.status_code == HTTPStatus.ACCEPTED
