class UserService:
    @staticmethod
    def onboard_user(data):
        username = data.get("username", "Guest")
        return {
            "status": "success",
            "message": f"Welcome {username}! Onboarding successful.",
            "user_id": 123
        }

    @staticmethod
    def get_favourites(user_id=None):
        return {
            "user_id": user_id,
            "favourites": ["Movie A", "Movie B"],
            "message": "Getting favourite movies success"
        }

    @staticmethod
    def add_to_favourites(user_id, movie_id):
        return {
            "status": "success",
            "movie_id": movie_id,
            "message": "Adding movie to favourite success"
        }