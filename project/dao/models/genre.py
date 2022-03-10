from coursework_3_source.project.dao.models.base import BaseMixin
from coursework_3_source.project.setup_db import db


class Genre(BaseMixin, db.Model):
    __tablename__ = "genres"

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre '{self.name.title()}'>"
