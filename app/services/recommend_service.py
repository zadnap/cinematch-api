from ml.inference.recommender import recommend_movies

class RecommendService:
    @staticmethod
    def recommend(user_id, top_k=200):
        top_tmdb_ids = recommend_movies(int(user_id), top_k)
        return top_tmdb_ids