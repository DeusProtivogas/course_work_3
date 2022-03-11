from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    # def get_all(self):
    #     return self._db_session.query(Genre).all()

    def get_all(self, filters):
        # А еще можно сделать так, вместо всех методов get_by_*
        t = self._db_session.query(Movie)
        if "status" in filters and filters.get("status") is not None:
            # print(filters.get("status"))
            if filters.get("status") == "new":
                t = t.order_by(desc(Movie.year))
        if "page" in filters and filters.get("page") is not None:
            # print(filters.get("page"))
            t = t.paginate(page=int(filters.get("page")), per_page=12).items
            # print(type(t))
            return t
        #     t = t.filter(Movie.genre_id == filters.get("genre_id"))
        # if "year" in filters:
        #     t = t.filter(Movie.year == filters.get("year"))
        # return t.all()
        return t.all() # self._db_session.query(Movie).all()

    def get_by_director_id(self, val):
        return self._db_session.query(Movie).filter(Movie.director_id == val).all()

    def get_by_genre_id(self, val):
        return self._db_session.query(Movie).filter(Movie.genre_id == val).all()

    def get_by_year(self, val):
        return self._db_session.query(Movie).filter(Movie.year == val).all()

    def create(self, movie_d):
        ent = Movie(**movie_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def delete(self, rid):
        movie = self.get_by_id(rid)
        self._db_session.delete(movie)
        self._db_session.commit()

    def update(self, movie_d):
        movie = self.get_by_id(movie_d.get("id"))
        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()
