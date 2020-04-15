from random import randint
from threading import Thread
from time import sleep
from typing import Any, Callable, Dict, List, Tuple

from exchange.models import Currencies, Operation, User, UserPackage
from exchange.response_statuses import ResponseStatus

is_base_locked = False


def run(session: Any) -> None:
    session.add_all(
        [
            Currencies('CU', 1, 1),
            Currencies('USD', 76, 78),
            Currencies('EUR', 82, 85),
            Currencies('CHF', 78, 80),
            Currencies('GBP', 82, 83),
            Currencies('KGS', 10, 12),
        ]
    )
    session.commit()
    thread = Thread(target=change_exchange_rates, args=(session,))
    thread.daemon = True
    thread.start()


def base_operation(operation: Any) -> Callable[[Any], Any]:
    def wrapper(*args):
        global is_base_locked

        while is_base_locked:
            continue
        is_base_locked = True

        res = operation(*args)

        is_base_locked = False
        return res

    return wrapper


def change_exchange_rates(session: Any) -> None:
    while True:
        sleep(10)
        print('lol')
        change_rates(session)


@base_operation
def change_rates(session: Any) -> None:
    for currency in session.query(Currencies):
        r = randint(-10, 10)
        if currency.name == 'CU':
            continue
        currency.purchase_rate = int(currency.purchase_rate * (100 - r) / 100)
        currency.selling_rate = int(currency.selling_rate * (100 - r) / 100)
    session.commit()


@base_operation
def registration(session: Any, name: str) -> None:
    user = User(name)
    session.add(user)
    session.flush()

    currencies = session.query(Currencies).filter_by(name='CU').first()

    user_package = UserPackage(user.id, currencies.id, 1000)
    session.add(user_package)
    session.commit()


@base_operation
def add_currency(
    session: Any, currencies_name: str, selling_rate: int, purchase_rate: int
) -> None:
    currency = Currencies(currencies_name, selling_rate, purchase_rate)
    session.add(currency)
    session.commit()


@base_operation
def get_currencies_rate(session: Any, currencies_name: str) -> Dict[str, Any]:
    currency = session.query(Currencies).filter_by(name=currencies_name).first()
    return {
        'name': currency.name,
        'selling_rate': currency.selling_rate,
        'purchase_rate': currency.purchase_rate,
    }


@base_operation
def get_operations_list(session: Any, user_name: str) -> Dict[str, List[Any]] or Any:
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        return ResponseStatus.NU
    user_id = user.id
    operation_list = session.query(Operation).filter_by(user_id=user_id).all()
    result_list = []
    for line in operation_list:
        result_list.append(str(line))

    return {'operation_list': result_list}


def bd_update(
    session: Any,
    currency_new: Tuple[Any, Any],
    user_and_currency: Tuple[Any, Any],
    count: int,
) -> None:

    session.add(currency_new[0])
    session.add(currency_new[1])
    session.add(
        Operation(user_and_currency[0].id, 'buy', user_and_currency[1].name, count)
    )
    session.commit()


def check_currency(
    session: Any, user_name: str, currencies_name: str
) -> Any or Tuple[Any]:
    currency = session.query(Currencies).filter_by(name=currencies_name).first()

    if not currency:
        return ResponseStatus.NC

    user = session.query(User).filter_by(name=user_name).first()
    c_u_id = session.query(Currencies).first().id

    return currency, user, c_u_id


@base_operation
def buy_currency(session: Any, user_name: str, currencies_name: str, count: int) -> Any:
    res = check_currency(session, user_name, currencies_name)

    try:
        currency, user, c_u_id = res[0], res[1], res[2]
    except TypeError:
        return res

    rate = currency.purchase_rate
    c_u_balance = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == c_u_id)
        .first()
    )

    if c_u_balance.amount < count * rate:
        return ResponseStatus.IF

    current_balance_i = c_u_balance.amount - count * rate

    session.commit()

    currency_table = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == currency.id)
        .first()
    )

    if not currency_table:
        currency_new = UserPackage(user.id, currency.id, count)

    else:
        current_balance_cur = (
            session.query(UserPackage)
            .filter(
                UserPackage.user_id == user.id, UserPackage.currency_id == currency.id
            )
            .first()
        )
        current_balance_currency = current_balance_cur.amount + count
        currency_new = (
            session.query(UserPackage)
            .filter(
                UserPackage.user_id == user.id, UserPackage.currency_id == currency.id
            )
            .first()
        )
        currency_new.amount = current_balance_currency

    c_u = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == c_u_id)
        .first()
    )
    c_u.amount = current_balance_i

    bd_update(session, (currency_new, c_u), (user, currency), count)

    return ResponseStatus.CB.value


@base_operation
def sell_currency(
    session: Any, user_name: str, currencies_name: str, count: int
) -> Any:
    res = check_currency(session, user_name, currencies_name)

    try:
        currency, user, c_u_id = res[0], res[1], res[2]
    except TypeError:
        return res

    currency_table = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == currency.id)
        .first()
    )

    if not currency_table:
        return ResponseStatus.NC

    c_u_id = session.query(Currencies).first().id
    rate = currency.selling_rate

    if currency_table.amount < count:
        return ResponseStatus.IF

    current_balance_currency = currency_table.amount - count

    session.commit()

    current_balance_cu = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == c_u_id)
        .first()
        .amount
    )
    current_balance_cu += count * rate

    currency_new = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == currency.id)
        .first()
    )
    currency_new.amount = current_balance_currency

    c_u = (
        session.query(UserPackage)
        .filter(UserPackage.user_id == user.id, UserPackage.currency_id == c_u_id)
        .first()
    )
    c_u.amount = current_balance_cu

    bd_update(session, (currency_new, c_u), (user, currency), count)

    return ResponseStatus.CS.value
