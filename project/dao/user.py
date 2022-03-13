from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def delete(self, rid):
        user = self.get_by_id(rid)
        self._db_session.delete(user)
        self._db_session.commit()

    def update(self, user_d):
        user = self.get_by_id(user_d.get("id"))
        user.name = user_d.get("name")
        user.surname = user_d.get("surname")

        self._db_session.add(user)
        self._db_session.commit()
        return user


    def update_password(self, user_d):
        user = self.get_by_id(user_d.get("id"))
        user.password = user_d.get("password2")

        self._db_session.add(user)
        self._db_session.commit()
        return user