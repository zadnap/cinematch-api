from app.clients.tmdb_client import TMDBClient
from app.utils.pagination import normalize_page

class MovieService:
    @staticmethod
    def get_details(movie_id):
        return {"movie_id": movie_id, "title": "Example Movie", "status": "success"}


    @staticmethod
    def get_trending(page=1):
        page = normalize_page(page)
        try:
            data = TMDBClient.get("/movie/popular", {"page": page})
            movies = [
                {
                    "id": m.get("id"),
                    "posterSrc": (
                        f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
                        if m.get("poster_path")
                        else None
                    ),
                    "title": m.get("title"),
                    "year": m.get("release_date", "")[:4] if m.get("release_date") else None,
                    "rating": round(m.get("vote_average", 0), 1),
                }
                for m in data.get("results", [])
            ]

            return {
                "success": True,
                "movies": movies,
                "total_pages": normalize_page(data.get("total_pages", 1))
            }
        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {"success": False, "error": {
                "message": "Failed to fetch trending movies"
            }}


    @staticmethod
    def search_movies(query=None):
        return {"message": f"Searching success for: {query}"}


    @staticmethod
    def get_by_genre(genre):
        return {"genre": genre, "movies": []}


    @staticmethod
    def get_upcoming(page=1):
        page = normalize_page(page)
        try:
            data = TMDBClient.get("/movie/upcoming", {"page": page})
            movies = [
                {
                    "id": m.get("id"),
                    "posterSrc": (
                        f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
                        if m.get("poster_path")
                        else None
                    ),
                    "title": m.get("title"),
                    "year": m.get("release_date", "")[:4] if m.get("release_date") else None,
                    "rating": round(m.get("vote_average", 0), 1),
                }
                for m in data.get("results", [])
            ]

            return {
                "success": True,
                "movies": movies,
                "total_pages": normalize_page(data.get("total_pages", 1))
            }
        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {"success": False, "error": {
                "message": "Failed to fetch upcoming movies"
            }}


    @staticmethod
    def get_trailers():
        return {"message": "Getting trailers success"}