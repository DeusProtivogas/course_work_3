from coursework_3_source.project.dao.models.base import BaseMixin
from coursework_3_source.project.setup_db import db


class Director(BaseMixin, db.Model):
    __tablename__ = 'directors'

    name = db.Column(db.String(255))

    def __repr__(self):
        return f"<Director {self.name.title()}>"