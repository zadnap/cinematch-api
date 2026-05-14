from app.models import User, Favourite, Movie
from init_db import GENRES
from sqlalchemy.orm import joinedload
from app.utils.format_genre import format_genres
from app.utils.response import success, error

class TrainingDataService:
    @staticmethod
    def get_user_features(user_id):
        try:
            user = User.query.get(user_id)

            if not user:
                return error(
                    "USER_NOT_FOUND",
                    f"User {user_id} not found",
                    404
                )

            pref_map = {
                pref.genre_id: pref.avg_score
                for pref in user.genre_preferences
            }

            avg_vector = [
                pref_map.get(gid, 0.0)
                for gid, _ in GENRES
            ]

            result = [user_id] + avg_vector

            return success(
                result,
                "User features fetched successfully"
            )

        except Exception as e:
            print(f"[GET USER FEATURES ERROR] {e}")

            return error(
                "SERVER_ERROR",
                "Server error",
                500
            )


    @staticmethod
    def get_all_user_features():
        try:
            users = User.query.all()

            result = []

            for user in users:
                pref_map = {
                    pref.genre_id: pref.avg_score
                    for pref in user.genre_preferences
                }

                avg_vector = [
                    pref_map.get(gid, 0.0)
                    for gid, _ in GENRES
                ]

                row = [user.id] + avg_vector

                result.append(row)

            return success(
                result,
                "All user features fetched successfully"
            )

        except Exception as e:
            print(f"[GET ALL USER FEATURES ERROR] {e}")

            return error(
                "SERVER_ERROR",
                "Server error",
                500
            )


    @staticmethod
    def get_ratings():
        try:
            favourites = Favourite.query.all()

            result = [
                [
                    fav.user_id,
                    fav.movie_id,
                    int(fav.added_at.timestamp())
                ]
                for fav in favourites
            ]

            return success(
                result,
                "Ratings fetched successfully"
            )

        except Exception as e:
            print(f"[GET RATINGS ERROR] {e}")

            return error(
                "SERVER_ERROR",
                "Server error",
                500
            )


    @staticmethod
    def get_favourite_movies():
        try:
            movies = (
                Movie.query
                .options(joinedload(Movie.genres))
                .all()
            )

            result = [
                [
                    movie.id,
                    (
                        f"{movie.title} ({movie.release_year})"
                        if movie.release_year
                        else movie.title
                    ),
                    format_genres(movie.genres)
                ]
                for movie in movies
            ]

            return success(
                result,
                "Favourite movies fetched successfully"
            )

        except Exception as e:
            print(f"[GET FAVOURITE MOVIES ERROR] {e}")

            return error(
                "SERVER_ERROR",
                "Server error",
                500
            )