from ml.inference.recommender import recommend_movies
from app.models import db, UserGenrePreference

class RecommendService:
    @staticmethod
    def recommend(user_id, top_k=200):
        top_tmdb_ids = recommend_movies(int(user_id), top_k)
        return top_tmdb_ids
    

    @staticmethod
    def onboard(user_id, genres, movies):
        # add 4.0 to avg_score when choose genre
        for genre_id in genres:
            new_pref = UserGenrePreference(
                user_id=user_id,
                genre_id=genre_id,
                avg_score=4.0
            )
            db.session.add(new_pref)

        # get genres in movie
        for movie in movies:
            movie_genres = movie.get('genres', [])
            
            # add 0.5 avg_score if avg_score < 5.0 to make sure it must <= 5.0
            for g_id in movie_genres:
                existing_pref = UserGenrePreference.query.filter_by(
                    user_id=user_id, 
                    genre_id=g_id
                ).first()

                if existing_pref:
                    if existing_pref.avg_score < 5.0:
                        existing_pref.avg_score += 0.5
                else:
                    new_pref = UserGenrePreference(
                        user_id=user_id,
                        genre_id=g_id,
                        avg_score=0.5
                    )
                    db.session.add(new_pref)

        db.session.commit()
        