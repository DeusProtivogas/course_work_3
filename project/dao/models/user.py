from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(255), default="Ivan")
    surname = db.Column(db.String(255), default="Ivanov")
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genres.id"))
    genre = db.relationship("Genre")

    def __repr__(self):
        return f"<User {self.name.title()} {self.surname.title()}>"
