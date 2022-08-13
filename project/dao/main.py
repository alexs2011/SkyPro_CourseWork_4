from typing import List, Optional

from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_sorted(self, page: Optional[int] = None, is_sorted=False) -> List[Movie]:
        stmt = self._db_session.query(self.__model__)
        if is_sorted:
            stmt = stmt.order_by(desc(self.__model__.year))

        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, login, password_hash):
        try:
            self._db_session.add(
                User(
                    email=login,
                    password=password_hash
                )
            )
            self._db_session.commit()
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_login(self, login):
        try:
            stmt = self._db_session.query(self.__model__).filter(self.__model__.email == login).one()
            return stmt
        except Exception as e:
            print(e)
            return {}

    def update(self, login, data):
        try:
            stmt = self._db_session.query(self.__model__).filter(self.__model__.email == login).update(data)
            self._db_session.commit()
            return stmt
        except Exception as e:
            print(e)
            self._db_session.rollback()
