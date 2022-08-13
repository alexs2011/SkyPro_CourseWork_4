from typing import Optional

from project.dao.main import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import approve_refresh_token, generate_password_hash, generate_tokens, get_data_from_token


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create_user(self, data):
        login = data.get('email')
        password_hash = generate_password_hash(data['password'])
        self.dao.create(login, password_hash)

    def login_user(self, username, password):
        return generate_tokens(self.dao, username, password)

    def update_user_session(self, ref_token):
        return approve_refresh_token(self.dao, ref_token)

    def get_user_by_token(self, ref_token):
        data = get_data_from_token(ref_token)
        if not data:
            return None

        return self.dao.get_user_by_login(data.get('email'))

    def update_user(self, ref_token, data):
        user = self.get_user_by_token(ref_token)
        if not user:
            return False
        return self.dao.update(user.email, data)

    def update_password(self, ref_token, data):
        user = self.get_user_by_token(ref_token)
        if not user:
            return False
        password_hash = generate_password_hash(data['password_2'])
        self.dao.update(login=user.email, data={'password': password_hash})
        return self.login_user(user.email, data['password_2'])

