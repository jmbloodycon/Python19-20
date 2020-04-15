from base64 import b64encode
from http import HTTPStatus

import movies.api as flaskr
import pytest
from flask import json


@pytest.fixture(scope='session')
def client():
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        yield client


def msg(method, description):
    return {"jsonrpc": "2.0", "id": "1", "method": method, "params": description}


def test_add_comment(client):
    massage = msg(
        'add_comment', {'name_film': 'Вперед', 'username': 'lol', 'comment': 'kek'}
    )
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['result'] == 'comment add'


def test_rate_film(client):
    massage = msg('rate_film', {'name_film': 'Вперед', 'username': 'lol', 'rate': 6})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['result'] == 'Movie rated'


def test_get_rating(client):
    massage = msg('get_rating', {'name_film': 'Начало', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['result'] == 0.0


def test_get_ratings_count(client):
    massage = msg('get_ratings_count', {'name_film': 'Начало', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['result'] == 0


def test_get_comments_count(client):
    massage = msg('get_comments_count', {'name_film': 'Начало', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['result'] == 0


def test_films_by_year(client):
    massage = msg('get_films_by_year', {'year': 2010, 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert len(data['result']) == 3


def test_top_films(client):
    massage = msg('get_top_films', {'rate': 1, 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert len(data['result']) == 1


def test_film_by_substring(client):
    massage = msg('get_films_by_substring', {'substring': 'Нач', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    data = json.loads(mas.get_data(as_text=True))
    assert len(data['result']) == 1


def test_not_found(client):
    massage = msg('get_lol', {'substring': 'Нач', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    assert mas.status_code == HTTPStatus.NOT_FOUND


def test_bad_request_get_ratings_count(client):
    massage = msg('get_ratings_count', {'name_film': 'Начал', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    assert mas.status_code == HTTPStatus.BAD_REQUEST


def test_bad_request_add_comment(client):
    massage = msg(
        'add_comment', {'name_film': 'Впед', 'username': 'lol', 'comment': 'kek'}
    )
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    assert mas.status_code == HTTPStatus.BAD_REQUEST


def test_bad_request_rate_film(client):
    massage = msg('rate_film', {'name_film': 'Вперед', 'username': 'lol', 'rate': 11})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    assert mas.status_code == HTTPStatus.BAD_REQUEST


def test_bad_request_get_comments_count(client):
    massage = msg('get_comments_count', {'name_film': 'Наало', 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    assert mas.status_code == HTTPStatus.BAD_REQUEST


def test_bad_request_top_films(client):
    massage = msg('get_top_films', {'rat': 1, 'username': 'lol'})
    mas = client.post(
        '/movies',
        data=json.dumps(massage),
        content_type='application/json',
        headers={"Authorization": b64encode(b'lol:kek')},
    )
    assert mas.status_code == HTTPStatus.BAD_REQUEST
