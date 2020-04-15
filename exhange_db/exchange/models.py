import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserPackage(Base):
    __tablename__ = 'users_package'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    amount = Column(Integer)

    def __init__(self, user_id: int, currency_id: int, amount: int) -> None:
        self.user_id = user_id
        self.currency_id = currency_id
        self.amount = amount


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_package = relationship('Currencies', secondary='users_package')
    users_operations = relationship('Operation', backref='users')

    def __init__(self, name: str) -> None:
        self.name = name


class Currencies(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    selling_rate = Column(Integer)
    purchase_rate = Column(Integer)

    def __init__(self, name: str, selling_rate: int, purchase_rate: int) -> None:
        self.name = name
        self.selling_rate = selling_rate
        self.purchase_rate = purchase_rate


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    operations_type = Column(String)
    currency = Column(String)
    count = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(
        self, user_id: int, operation_type: str, currency: str, count: int
    ) -> None:
        self.user_id = user_id
        self.operations_type = operation_type
        self.currency = currency
        self.count = count

    def __repr__(self) -> str:
        return f'{self.operations_type}, {self.currency}, {self.count}, {self.created_date}'
