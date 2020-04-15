from os import path, remove
from typing import Any

from exchange.bd import (
    add_currency,
    buy_currency,
    get_currencies_rate,
    get_operations_list,
    registration,
    run,
    sell_currency,
)
from exchange.models import Base
from exchange.response_statuses import ResponseStatus
from flask import Flask, abort, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
operations_list = []

if path.exists('currencies.db'):
    remove('currencies.db')
engine = create_engine('sqlite:///currencies.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
Session.configure(bind=engine)
session = Session()

run(session)


@app.route('/exchange/currencies_rate/<string:currency_name>', methods=['GET'])
def currencies_rate(currency_name: str) -> Any:
    return jsonify(get_currencies_rate(session, currency_name))


@app.route('/exchange/operation_list/<string:username>', methods=['GET'])
def get_operation(username: str) -> Any:
    return jsonify(get_operations_list(session, username))


@app.route('/exchange/registration', methods=['POST'])
def register() -> Any:
    if not request.json or 'username' not in request.json:
        abort(400)
    registration(session, request.json['username'])
    return jsonify({'status': ResponseStatus.UA.value}), 201


@app.route('/exchange/add_currency', methods=['POST'])
def add_curr() -> Any:
    if (
        not request.json
        or 'curr_name' not in request.json
        or 'sell_rate' not in request.json
        or 'push_rate' not in request.json
    ):
        abort(400)

    add_currency(
        session,
        request.json['curr_name'],
        request.json['sell_rate'],
        request.json['push_rate'],
    )
    return jsonify({'status': ResponseStatus.CA.value}), 201


@app.route('/exchange/buy_currency', methods=['PUT'])
def buy_curr() -> Any:
    if (
        not request.json
        or 'curr_name' not in request.json
        or 'username' not in request.json
        or 'count' not in request.json
    ):
        abort(400)

    res = buy_currency(
        session,
        request.json['username'],
        request.json['curr_name'],
        request.json['count'],
    )

    if res in (ResponseStatus.IF, ResponseStatus.NC):
        return jsonify({'error': res.value}), 400

    return jsonify({'status': res}), 200


@app.route('/exchange/sell_currency', methods=['PUT'])
def cell_curr() -> Any:
    if (
        not request.json
        or 'curr_name' not in request.json
        or 'username' not in request.json
        or 'count' not in request.json
    ):
        abort(400)

    res = sell_currency(
        session,
        request.json['username'],
        request.json['curr_name'],
        request.json['count'],
    )
    if res in (ResponseStatus.IF, ResponseStatus.NC):
        return jsonify({'error': res.value}), 400

    return jsonify({'status': res}), 200
