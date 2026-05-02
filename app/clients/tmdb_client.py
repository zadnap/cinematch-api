import os
import requests

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    @staticmethod
    def get(endpoint, params=None):
        API_KEY = os.getenv("TMDB_API_KEY")

        if not API_KEY:
            raise Exception("Missing TMDB API key")

        if params is None:
            params = {}

        params["api_key"] = API_KEY
        params["language"] = "en-US"

        url = f"{TMDBClient.BASE_URL}{endpoint}"

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        return response.json()