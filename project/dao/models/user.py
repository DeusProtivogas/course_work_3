from coursework_3_source.project.dao.models.base import BaseMixin
from coursework_3_source.project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    # favorite_genre

