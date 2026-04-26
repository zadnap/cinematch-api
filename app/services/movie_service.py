class MovieService:
    @staticmethod
    def get_details(movie_id):
        return {"movie_id": movie_id, "title": "Example Movie", "status": "success"}

    @staticmethod
    def get_trending():
        return {"message": "Getting trending success"}

    @staticmethod
    def search_movies(query=None):
        return {"message": f"Searching success for: {query}"}

    @staticmethod
    def get_by_genre(genre):
        return {"genre": genre, "movies": []}

    @staticmethod
    def get_upcoming():
        return {"message": "Getting upcoming movies success"}

    @staticmethod
    def get_trailers():
        return {"message": "Getting trailers success"}