from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Genre


class GenreDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Genre).filter(Genre.id == pk).one_or_none()

    def get_all(self, filters):
        t = self._db_session.query(Genre)
        if "page" in filters and filters.get("page") is not None:
            t = t.paginate(page=int(filters.get("page")), per_page=12).items
            return t
        return t.all()
