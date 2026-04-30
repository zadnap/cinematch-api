from app.clients.tmdb_client import TMDBClient
from concurrent.futures import ThreadPoolExecutor
from app.utils.pagination import normalize_page
from app.services.recommend_service import RecommendService
from app.utils.rerank_movies import rerank_movies

class MovieService:
    @staticmethod
    def get_details(movie_id):
        try:
            def fetch(endpoint):
                return TMDBClient.get(endpoint)

            with ThreadPoolExecutor(max_workers=5) as executor:
                movie_data, credits_data, release_data, video_data, review_data = executor.map(
                    fetch,
                    [
                        f"/movie/{movie_id}",
                        f"/movie/{movie_id}/credits",
                        f"/movie/{movie_id}/release_dates",
                        f"/movie/{movie_id}/videos",
                        f"/movie/{movie_id}/reviews",
                    ],
                )
            us_release = next(
                (r for r in release_data.get("results", []) if r.get("iso_3166_1") == "US"),
                None,
            )
            certification = "NR"
            if us_release:
                cert = next(
                    (r.get("certification") for r in us_release.get("release_dates", []) if r.get("certification")),
                    None,
                )
                if cert:
                    certification = cert
            trailer = next(
                (
                    v for v in video_data.get("results", [])
                    if v.get("type") == "Trailer" and v.get("site") == "YouTube"
                ),
                None,
            )
            movie = {
                "id": movie_data.get("id"),
                "title": movie_data.get("title"),
                "posterSrc": (
                    f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}"
                    if movie_data.get("poster_path") else None
                ),
                "backdropSrc": (
                    f"https://image.tmdb.org/t/p/original{movie_data.get('backdrop_path')}"
                    if movie_data.get("backdrop_path") else None
                ),
                "certification": certification,
                "releaseDate": movie_data.get("release_date"),
                "duration": movie_data.get("runtime"),
                "overview": movie_data.get("overview"),
                "genres": movie_data.get("genres", []),
                "rating": round(movie_data.get("vote_average", 0), 1),
                "languages": [
                    {
                        "id": lang.get("iso_639_1"),
                        "name": lang.get("english_name"),
                    }
                    for lang in movie_data.get("spoken_languages", [])
                ],
                "directors": [
                    p.get("name")
                    for p in credits_data.get("crew", [])
                    if p.get("job") == "Director"
                ],
                "writers": [
                    p.get("name")
                    for p in credits_data.get("crew", [])
                    if p.get("job") in ["Writer", "Screenplay", "Author", "Story"]
                ],
                "trailerKey": trailer.get("key") if trailer else None,
            }
            casts = [
                {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "character": c.get("character"),
                    "profilePicture": (
                        f"https://image.tmdb.org/t/p/w185{c.get('profile_path')}"
                        if c.get("profile_path") else None
                    ),
                }
                for c in credits_data.get("cast", [])
            ]
            reviews = [
                {
                    "id": r.get("id"),
                    "author": r.get("author"),
                    "detail": r.get("content"),
                    "rating": (r.get("author_details", {}).get("rating") or 0) * 10,
                    "profileImage": (
                        f"https://image.tmdb.org/t/p/w92{r.get('author_details', {}).get('avatar_path')}"
                        if r.get("author_details", {}).get("avatar_path") else None
                    ),
                    "releaseDate": r.get("created_at"),
                }
                for r in review_data.get("results", [])
            ]

            return {
                "success": True,
                "movie": movie,
                "casts": casts,
                "reviews": reviews,
            }

        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to fetch movie details"
                }
            }


    @staticmethod
    def get_trending(page, user_id=None):
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

            if user_id:
                rec_ids = RecommendService.recommend(user_id, top_k=200)
                movies = rerank_movies(movies, rec_ids)

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
    def search_movies(query, page=1):
        page = normalize_page(page)
        try:
            if not query:
                return {
                    "success": False,
                    "error": {"message": "Missing search query"}
                }

            data = TMDBClient.get(
                "/search/movie",
                {
                    "query": query,
                    "page": page,
                    "language": "en-US"
                }
            )
            results = data.get("results", [])
            movies = [
                {
                    "id": m.get("id"),
                    "title": m.get("title"),
                    "year": m.get("release_date", "")[:4] if m.get("release_date") else None,
                    "rating": round(m.get("vote_average", 0), 1),
                    "posterSrc": (
                        f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
                        if m.get("poster_path") else None
                    ),
                }
                for m in results
            ]
            if not movies:
                return {
                    "success": False,
                    "error": {
                        "message": f"Could not find movies named '{query}'"
                    }
                }

            return {
                "success": True,
                "movies": movies,
                "total_pages": normalize_page(data.get("total_pages", 1))
            }

        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to search movies"
                }
            }


    @staticmethod
    def get_genres():
        try:
            data = TMDBClient.get("/genre/movie/list", {"language": "en-US"})

            return {
                "success": True,
                "genres": data.get("genres", [])
            }

        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to fetch genres"
                }
            }
        

    @staticmethod
    def get_by_genres(genre_ids, page, user_id=None):
        page = normalize_page(page)
        try:
            genre_string = ",".join(genre_ids)
            data = TMDBClient.get(
                "/discover/movie",
                {
                    "with_genres": genre_string,
                    "page": page
                }
            )
            movies = [
                {
                    "id": m.get("id"),
                    "title": m.get("title"),
                    "year": m.get("release_date", "")[:4] if m.get("release_date") else None,
                    "rating": round(m.get("vote_average", 0), 1),
                    "posterSrc": (
                        f"https://image.tmdb.org/t/p/w342{m.get('poster_path')}"
                        if m.get("poster_path") else None
                    ),
                }
                for m in data.get("results", [])
            ]
            if user_id:
                rec_ids = RecommendService.recommend(user_id, top_k=200)
                movies = rerank_movies(movies, rec_ids)

            return {
                "success": True,
                "movies": movies,
                "total_pages": normalize_page(data.get("total_pages", 1))
            }

        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to fetch movies by genres"
                }
            }
        
    @staticmethod
    def get_by_multiple_genres(genre_ids, page, user_id):
        page = normalize_page(page)


    @staticmethod
    def get_upcoming(page, user_id=None):
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

            if user_id:
                rec_ids = RecommendService.recommend(user_id, top_k=200)
                movies = rerank_movies(movies, rec_ids)

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
        
    
    @staticmethod
    def get_featured_movie():
        try:
            def fetch(endpoint, params=None):
                return TMDBClient.get(endpoint, params)
            with ThreadPoolExecutor(max_workers=2) as executor:
                popular_data, genre_data = executor.map(
                    lambda args: fetch(*args),
                    [
                        ("/movie/popular", {"language": "en-US", "page": 1}),
                        ("/genre/movie/list", {"language": "en-US"}),
                    ],
                )
            movies = popular_data.get("results", [])
            genres = genre_data.get("genres", [])

            if not movies:
                raise Exception("No popular movies found")
            
            movie = movies[0]
            genre_map = {g["id"]: g["name"] for g in genres}
            tags = [
                movie.get("release_date", "")[:4],
                *[
                    genre_map.get(gid)
                    for gid in movie.get("genre_ids", [])
                    if genre_map.get(gid)
                ],
            ]
            result = {
                "id": movie.get("id"),
                "title": movie.get("title"),
                "desc": movie.get("overview"),
                "tags": tags,
                "backdropSrc": (
                    f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path')}"
                    if movie.get("backdrop_path")
                    else None
                ),
            }

            return {
                "success": True,
                "movie": result
            }

        except Exception as e:
            print(f"[TMDB ERROR] {e}")
            return {
                "success": False,
                "error": {
                    "message": "Failed to fetch featured movie"
                }
            }