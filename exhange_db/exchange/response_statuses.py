from enum import Enum


class ResponseStatus(Enum):
    IF = 'Insufficient funds'
    NC = 'Nonexistent currency'
    NU = 'Nonexistent user'
    UA = 'User added'
    CA = 'New currency added'
    CB = 'Currency purchased'
    CS = 'Currency sold'
