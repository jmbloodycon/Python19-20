from typing import Dict

from werkzeug.security import check_password_hash, generate_password_hash


class Users:
    def __init__(self) -> None:
        self.users: Dict[str, str] = {}

    def create_user(self, name: str, password: str) -> None:
        self.users[name] = generate_password_hash(password)

    def check_user_existence(self, username: str) -> bool:
        return username in self.users

    def check_user_password(self, user: str, password: str) -> bool:
        return check_password_hash(self.users[user], password)
