from app import db
from app.models import User, Favourite
from app.clients.tmdb_client import TMDBClient
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def onboard_user(user_id, genres, movies):
        user = User.query.get(user_id)

        if not user:
            return {"success": False, "message": "User not found"}, 404
        
        user.is_onboarded = True
        
        db.session.commit()

        return {"success": True}, 200

    @staticmethod
    def get_favourites(user_id, page=1, per_page=20):
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": {
                        "message": "User not found"
                    }
                }
            pagination = Favourite.query\
                .filter_by(user_id=user_id)\
                .order_by(Favourite.added_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)
            tmdb_ids = [f.tmdb_id for f in pagination.items]

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
                except:
                    return None 

            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(fetch_movie, tmdb_ids))

            movies = [m for m in results if m] 

            return {
                "success": True,
                "favourites": movies,
                "page": page,
                "total_pages": pagination.pages
            }

        except Exception as e:
            print(f"[FAVOURITES ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to fetch favourite movies"
                }
            }

    @staticmethod
    def add_to_favourites(user_id, movie_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": {
                        "message": "User not found"
                    }
                }
            favourite = Favourite(
                user_id=user_id,
                tmdb_id=movie_id
            )
            db.session.add(favourite)
            db.session.commit()
            return {
                "success": True,
                "movie_id": movie_id,
                "message": "Added movie to favourites successfully"
            }

        except IntegrityError:
            db.session.rollback()
            return {
                "success": True,
                "movie_id": movie_id,
                "message": "Movie already in favourites"
            }

        except Exception as e:
            db.session.rollback()
            print(f"[ADD FAVOURITE ERROR] {e}")

            return {
                "success": False,
                "error": {
                    "message": "Failed to add favourite movie"
                }
            }
        
    
    @staticmethod
    def check_favourite(user_id, movie_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": {
                        "message": "User not found"
                    }
                }

            existing = Favourite.query.filter_by(
                user_id=user_id,
                tmdb_id=movie_id
            ).first()

            return {
                "success": True,
                "isFavourite": existing is not None
            }

        except Exception as e:
            print(f"[CHECK FAVOURITE ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to check favourite"
                }
            }
        
    @staticmethod
    def remove_from_favourites(user_id, movie_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    "success": False,
                    "error": {
                        "message": "User not found"
                    }
                }

            favourite = Favourite.query.filter_by(
                user_id=user_id,
                tmdb_id=movie_id
            ).first()

            if not favourite:
                return {
                    "success": False,
                    "error": {
                        "message": "Favourite not found"
                    }
                }

            db.session.delete(favourite)
            db.session.commit()

            return {
                "success": True,
                "movie_id": movie_id,
                "message": "Removed from favourites successfully"
            }

        except Exception as e:
            db.session.rollback()
            print(f"[REMOVE FAVOURITE ERROR] {e}")

            return {
                "success": False,
                "error": {
                    "message": "Failed to remove favourite movie"
                }
            }
        
    @staticmethod
    def get_user_data(user_id):
        user = User.query.get(user_id)

        if not user:
            return {
                "success": False,
                "error": {
                    "message": "User does not exist"
                }
            }

        return {
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "is_onboarded": user.is_onboarded
            }
        }