from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, filters):
        movies = MovieDAO(self._db_session).get_all(filters)

        # if filters.get("director_id") is not None:
        #     movies = self.dao.get_by_director_id(filters.get("director_id"))
        # elif filters.get("genre_id") is not None:
        #     movies = self.dao.get_by_genre_id(filters.get("genre_id"))
        # elif filters.get("year") is not None:
        #     movies = self.dao.get_by_year(filters.get("year"))
        # else:
        #     movies = self.dao.get_all()
        # return movies

        return MovieSchema(many=True).dump(movies)
