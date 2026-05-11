from app.models import User, Favourite, Movie
from init_db import GENRES
from sqlalchemy.orm import joinedload
from app.utils.format_genre import format_genres

ID_OFFSET = 200947

class TrainingDataService:
    @staticmethod
    def get_user_features(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        pref_map = {
            pref.genre_id: pref.avg_score
            for pref in user.genre_preferences
        }
        avg_vector = [
            pref_map.get(gid, 0.0) for gid, _ in GENRES
        ]

        user_id = user_id + ID_OFFSET

        return [user_id] + avg_vector
    

    @staticmethod
    def get_all_user_features():
        users = User.query.all()
        result = []

        for user in users:
            try:
                row = TrainingDataService.get_user_features(user.id)
                result.append(row)
            except Exception as e:
                print(f"Skip user {user.id}: {e}")

        return result
    

    @staticmethod
    def get_ratings():
        favourites = Favourite.query.all()
        return [
            [
                fav.user_id + ID_OFFSET,
                fav.movie_id,
                int(fav.added_at.timestamp())
            ]
            for fav in favourites
        ]
    

    @staticmethod
    def get_favourite_movies():
        movies = (
            Movie.query
            .options(joinedload(Movie.genres))
            .all()
        )
        return [
            [
                movie.id,
                f"{movie.title} ({movie.release_year})" if movie.release_year else movie.title,
                format_genres(movie.genres)
            ]
            for movie in movies
        ]