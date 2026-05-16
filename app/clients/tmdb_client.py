import os
import requests

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    session = requests.Session()

    @staticmethod
    def get(endpoint, params=None):
        API_KEY = os.getenv("TMDB_API_KEY")

        if not API_KEY:
            raise Exception("Missing TMDB API key")

        params = params or {}

        params.update({
            "api_key": API_KEY,
            "language": "en-US"
        })

        response = TMDBClient.session.get(
            f"{TMDBClient.BASE_URL}{endpoint}",
            params=params,
            timeout=(3, 5)
        )

        response.raise_for_status()
        return response.json()