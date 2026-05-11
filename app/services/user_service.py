from app import db
from app.models import User, Favourite, Movie, Genre
from app.clients.tmdb_client import TMDBClient
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import IntegrityError
from app.utils.response import success, error
from app.models import db, UserGenrePreference

class UserService:
    @staticmethod
    def onboard_user(user_id, data):
        user = User.query.get(user_id)

        if not user:
            return error("USER_NOT_FOUND", "User not found", 404)
        
        if not data:
            return error("INVALID_ONBOARDING_DATA", "Invalid JSON")
        
        genres = data.get("genres")
        movies = data.get("movies")

        if not isinstance(genres, list):
            return error("INVALID_ONBOARDING_DATA", "Genres must be array")

        if not isinstance(movies, list):
            return error("INVALID_ONBOARDING_DATA", "Movies must be array")

        genres = list(set(genres))
        
        user.is_onboarded = True

        for genre_id in list(set(genres)):
            new_pref = UserGenrePreference(user_id=user_id, genre_id=genre_id, avg_score=4.0)
            db.session.add(new_pref)
            
        for movie_data in movies:
            movie_id = movie_data.get('id')
            movie_title = movie_data.get('title')
            movie_genres = movie_data.get('genres', []) 

            existing_movie = Movie.query.get(movie_id)
            if not existing_movie:
                new_movie = Movie(id=movie_id, title=movie_title)
                if movie_genres:
                    db_genres = Genre.query.filter(Genre.id.in_(movie_genres)).all()
                    new_movie.genres.extend(db_genres)
                db.session.add(new_movie)

            is_fav_exists = Favourite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    
            if not is_fav_exists:
                new_fav = Favourite(user_id=user_id, movie_id=movie_id)
                db.session.add(new_fav)
    
            for g_id in movie_genres:
                existing_pref = UserGenrePreference.query.filter_by(
                    user_id=user_id, 
                    genre_id=g_id
                ).first()

                if existing_pref:
                    if existing_pref.avg_score < 5.0:
                        existing_pref.avg_score += 0.5
                else:
                    new_pref = UserGenrePreference(user_id=user_id, genre_id=g_id, avg_score=0.5)
                    db.session.add(new_pref)

        try:
            db.session.commit()
            return success({}, "Onboarded successfully")
        except Exception as e:
            db.session.rollback()
            print(f"[ONBOARD ERROR] {e}")
            return error("ONBOARDING_ERROR", str(e), 500)


    @staticmethod
    def get_favourites(user_id, page=1, per_page=20):
        try:
            user = User.query.get(user_id)
            if not user:
                return error("USER_NOT_FOUND", "User not found", 404)
            pagination = Favourite.query\
                .filter_by(user_id=user_id)\
                .order_by(Favourite.added_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)
            movie_ids = [f.movie_id for f in pagination.items]

            def fetch_movie(movie_id):
                try:
                    data = TMDBClient.get(f"/movie/{movie_id}")

                    return {
                        "id": data.get("id"),
                        "posterSrc": (
                            f"https://image.tmdb.org/t/p/w342{data.get('poster_path')}"
                            if data.get("poster_path") else None
                        ),
                        "title": data.get("title"),
                        "year": data.get("release_date", "")[:4] if data.get("release_date") else None,
                        "rating": round(data.get("vote_average", 0), 1),
                    }
                except Exception as e:
                    print(f"[TMDB ERROR] {e}")
                    return None

            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(fetch_movie, movie_ids))

            movies = [m for m in results if m] 
            return success({
                "favourites": movies,
                "page": page,
                "total_pages": pagination.pages
            }, "Getting favourite movies successfully")

        except Exception as e:
            print(f"[FAVOURITES ERROR] {e}")
            return error("SERVER_ERROR", "Failed to fetch favourite movies", 500)


    @staticmethod
    def add_to_favourites(user_id, movie):
        movie_id = movie.get("id")
        title = movie.get("title")
        genre_ids = [g["id"] for g in movie.get("genres", [])]

        try:
            user = User.query.get(user_id)
            if not user:
                return error("USER_NOT_FOUND", "User not found", 404)

            existing_movie = Movie.query.get(movie_id)

            if not existing_movie:
                new_movie = Movie(
                    id=movie_id,
                    title=title
                )

                if genre_ids:
                    genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
                    new_movie.genres.extend(genres)

                db.session.add(new_movie)

            favourite = Favourite(
                user_id=user_id,
                movie_id=movie_id
            )

            db.session.add(favourite)
            db.session.commit()

            return success({}, "Added movie to favourites successfully")

        except IntegrityError as e:
            db.session.rollback()
            if "_user_movie_uc" in str(e.orig):
                return success({}, "Movie already in favourites")

            return error("DB_ERROR", "Database error", 500)

        except Exception as e:
            db.session.rollback()
            print(f"[ADD FAVOURITE ERROR] {e}")
            return error("SERVER_ERROR", "Failed to add favourite movie", 500)
        
    
    @staticmethod
    def check_favourite(user_id, movie_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return error("USER_NOT_FOUND", "User not found", 404)

            existing = Favourite.query.filter_by(
                user_id=user_id,
                movie_id=movie_id
            ).first()
            return success({ "is_favourite": existing is not None }, "Check for favourite movie successfully")

        except Exception as e:
            print(f"[CHECK FAVOURITE ERROR] {e}")
            return error("SERVER_ERROR", "Failed to check favourite", 500)
        

    @staticmethod
    def remove_from_favourites(user_id, movie_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return error("USER_NOT_FOUND", "User not found", 404)

            favourite = Favourite.query.filter_by(
                user_id=user_id,
                movie_id=movie_id
            ).first()
            if not favourite:
                return success({}, "Already removed or not found")

            db.session.delete(favourite)
            db.session.commit()
            return success({}, "Removed from favourites successfully")

        except Exception as e:
            db.session.rollback()
            print(f"[REMOVE FAVOURITE ERROR] {e}")
            return error("SERVER_ERROR", "Failed to remove favourite movie", 500)
        

    @staticmethod
    def get_user_data(user_id):
        user = User.query.get(user_id)
        if not user:
            return error("USER_NOT_FOUND", "User not found", 404)

        return success(
            { "id": user.id, "username": user.username, "is_onboarded": user.is_onboarded }, 
            "Getting user's data successfully"
        )