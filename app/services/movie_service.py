from app.clients.tmdb_client import TMDBClient
from concurrent.futures import ThreadPoolExecutor
from app.utils.pagination import normalize_page

class MovieService:
    @staticmethod
    def get_details(movie_id):
        return {"movie_id": movie_id, "title": "Example Movie", "status": "success"}


    @staticmethod
    def get_trending(page):
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
    def get_upcoming(page):
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
    def get_trailers(limit):
        try:
            data = TMDBClient.get("/movie/popular")
            movies = data.get("results", [])[:limit]

            def fetch_trailer(m):
                try:
                    video_data = TMDBClient.get(f"/movie/{m.get('id')}/videos")

                    trailer = next(
                        (
                            v for v in video_data.get("results", [])
                            if v.get("type") == "Trailer" and v.get("site") == "YouTube"
                        ),
                        None
                    )

                    if trailer:
                        return {
                            "id": m.get("id"),
                            "title": m.get("title"),
                            "year": m.get("release_date", "")[:4],
                            "rating": round(m.get("vote_average", 0), 1),
                            "backdropSrc": f"https://image.tmdb.org/t/p/w342{m.get('backdrop_path')}"
                            if m.get("backdrop_path") else None,
                            "trailerKey": trailer.get("key"),
                        }
                except:
                    return None

            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(fetch_trailer, movies))

            trailers = [r for r in results if r]

            return {"success": True, "trailers": trailers}

        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {"success": False, "error": {
                "message": "Failed to fetch upcoming movies"
            }}