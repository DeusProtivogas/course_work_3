from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(255), default="Ivan")
    surname = db.Column(db.String(255), default="Ivanov")
    # favorite_genre

    def __repr__(self):
        return f"<User {self.name.title()} {self.surname.title()} {self.password.title()} >"
