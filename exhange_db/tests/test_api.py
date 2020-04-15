import exchange.api as flaskr
import pytest
from flask import json


@pytest.fixture(scope='session')
def client():
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        yield client


def test_add_user(client):
    massage = {'username': 'lol'}
    mas = client.post(
        '/exchange/registration',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['status'] == 'User added'


def test_add_currency(client):
    massage = {'curr_name': 'EGY', 'sell_rate': 120, 'push_rate': 44}
    mas = client.post(
        '/exchange/add_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['status'] == 'New currency added'


def test_get_operations(client):
    username = {'username': 'Вася'}
    client.post(
        '/exchange/registration',
        data=json.dumps(username),
        content_type='application/json',
    )
    res = client.get('/exchange/operation_list/Вася', content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    assert len(data['operation_list']) == 0


def test_buy_currency(client):
    massage = {'curr_name': 'EUR', 'username': 'lol', 'count': 2}
    mas = client.put(
        '/exchange/buy_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['status'] == 'Currency purchased'


def test_buy_currency_to_existing(client):
    massage = {'curr_name': 'EUR', 'username': 'lol', 'count': 2}
    client.put(
        '/exchange/buy_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    mas = client.put(
        '/exchange/buy_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['status'] == 'Currency purchased'


def test_sell_currency(client):
    massage = {'curr_name': 'EUR', 'username': 'lol', 'count': 1}
    mas = client.put(
        '/exchange/sell_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['status'] == 'Currency sold'


def test_get_currencies_rate(client):
    mas = client.get('/exchange/currencies_rate/CU', content_type='application/json')
    data = json.loads(mas.get_data(as_text=True))
    assert data['name'] == 'CU'


def test_buy_bad_currency(client):
    massage = {'curr_name': 'EUR', 'username': 'lol', 'count': 1000}
    mas = client.put(
        '/exchange/buy_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['error'] == 'Insufficient funds'


def test_sell_bad_currency(client):
    massage = {'curr_name': 'EUs', 'username': 'lol', 'count': 1}
    mas = client.put(
        '/exchange/sell_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['error'] == 'Nonexistent currency'


def test_sell_bad_currency_cu(client):
    massage = {'curr_name': 'CU', 'username': 'lol', 'count': 10000}
    mas = client.put(
        '/exchange/sell_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    data = json.loads(mas.get_data(as_text=True))
    assert data['error'] == 'Insufficient funds'


def test_buy_currency_bad_request(client):
    massage = {'curr': 'EUR', 'username': 'lol', 'count': 2}
    mas = client.put(
        '/exchange/buy_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    assert mas.status_code == 400


def test_sell_currency_bad_request(client):
    massage = {'curr': 'EUR', 'username': 'lol', 'count': 1}
    data = client.put(
        '/exchange/sell_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    assert data.status_code == 400


def test_add_user_bad_request(client):
    massage = {'user': 'lol'}
    data = client.post(
        '/exchange/registration',
        data=json.dumps(massage),
        content_type='application/json',
    )
    assert data.status_code == 400


def test_add_currency_bad_request(client):
    massage = {'curr_e': 'EGY', 'sell_rate': 120, 'push_rate': 44}
    data = client.post(
        '/exchange/add_currency',
        data=json.dumps(massage),
        content_type='application/json',
    )
    assert data.status_code == 400
