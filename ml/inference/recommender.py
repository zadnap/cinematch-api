import numpy as np
import pandas as pd
import os
from ml.models.two_towers_model import (
    TwoTowerModel, user_model, movie_model
)

from ml.training.dataset_loader import (
    NUM_MOVIES, NUM_USERS,
    movie_dataset,
    interactions,
    user_features_df,
    movie_features_df
)

from ml.training.data_preprocessing import (
    movie2movie_encoded, movies_df,
    ratings_df
)

from app.services.trainning_data_service import ID_OFFSET, TrainingDataService

ARTIFACTS_PATH = "ml/artifacts"
PROCESSED_DATA_PATH = "ml/data/processed_data"
RAW_DATA_PATH = "ml/data/raw_data"

def prepare_global_movie_scores(ratings_df, movies_df, movie2movie_encoded):
    rating_counts = ratings_df.groupby('movieId').size().reset_index(name='num_ratings')
    ratings_avg = ratings_df.groupby('movieId')['rating'].mean().reset_index(name='avg_rating')
    
    movie_scores_df = pd.merge(rating_counts, movies_df, on='movieId')
    movie_scores_df = pd.merge(ratings_avg, movie_scores_df, on='movieId')
    
    # Tính score
    movie_scores_df['score'] = movie_scores_df['num_ratings'] * movie_scores_df['avg_rating']
    
    # Map encoded_id
    movie_scores_df['encoded_id'] = movie_scores_df['movieId'].map(movie2movie_encoded)
    
    # Sắp xếp theo điểm số giảm dần
    movie_scores_df = movie_scores_df.sort_values(by='score', ascending=False)
    
    return movie_scores_df

GLOBAL_MOVIE_SCORES = prepare_global_movie_scores(ratings_df, movies_df, movie2movie_encoded)

def get_best_k_films_for_user(user_id, k=10):
    liked_genres_set = set()
    # Kiểm tra xem user_id có trong bảng user features chưa
    user_exists = (user_features_df['user_id'] == user_id).any()
    
    if user_exists:
        user_row = user_features_df[user_features_df['user_id'] == user_id].iloc[0]
        genre_columns = [col for col in user_row.index if col.endswith('_avg')]
        user_genres_avg = user_row[genre_columns]
        liked_genres = user_genres_avg[user_genres_avg > 3.8].index.str.replace('_avg', '').tolist()
        liked_genres_set = set(liked_genres)
    else:
        user_features = TrainingDataService.get_user_features(user_id)[1:]  # Bỏ user_id
        genre_cols = user_features_df.columns[1:].str.replace('_avg', '')
        liked_genres = [
            genre for genre, score in zip(genre_cols, user_features) 
            if score > 3.8
        ]
        liked_genres_set = set(liked_genres)
    
    valid_genres = [genre for genre in liked_genres_set if genre in movie_features_df.columns]
    
    if not valid_genres:
        return GLOBAL_MOVIE_SCORES.head(k)["movieId"].tolist()
    
    mask = movie_features_df[valid_genres].sum(axis=1) > 0
    matching_encoded_ids_set = set(movie_features_df.loc[mask, 'movie_id'].tolist())

    filtered_movies = GLOBAL_MOVIE_SCORES[GLOBAL_MOVIE_SCORES['encoded_id'].isin(matching_encoded_ids_set)]
    final_result = filtered_movies.head(k)
    
    return final_result["movieId"].tolist()

def get_top_k_recommendations(model, target_user_id, all_movie_vectors, k=10):    
    user_vector = model.user_model.predict(
        np.array([target_user_id], dtype=np.int32),
        verbose=0
    )
    
    scores = np.dot(all_movie_vectors, user_vector.T).flatten()

    # Lọc bỏ các phim User đã xem/đánh giá
    watched_movie_ids = interactions[interactions['user_id'] == target_user_id]['movie_id'].values
    scores[watched_movie_ids] = -999.0
    
    top_k_indices = np.argsort(scores)[::-1][:k]
    top_k_scores = scores[top_k_indices]
    
    return top_k_indices, top_k_scores

def mapping_movie_id_to_tmdb_id(movie_ids):
    links_df = pd.read_csv(os.path.join(RAW_DATA_PATH, "links.csv"))
    result = links_df[links_df["movieId"].isin(movie_ids)].set_index("movieId").loc[movie_ids, "tmdbId"].tolist()
    return result

def cold_start_recommendation(user_id, top_k=10):
    print(f"Đang thực hiện đề xuất cold-start cho User ID {user_id}...")
    # Lấy top K phim phổ biến nhất
    best_k_film_ids = get_best_k_films_for_user(user_id, k=top_k)
    if __name__ == "__main__":
        print(f"TOP {top_k} PHIM DÀNH CHO USER {user_id}:")

        for i in range(top_k):
            
            # Dịch ngược ID
            real_movie_id = best_k_film_ids[i]
            
            movie_info = movies_df[movies_df['movieId'] == real_movie_id]
            title = movie_info['title'].values[0]
            genres = movie_info['genres'].values[0]
            
            print(f"{i+1:2d}. {title[:40]:<42} | Thể loại: {genres}")
    top_tmdb_ids = mapping_movie_id_to_tmdb_id(best_k_film_ids)
    return top_tmdb_ids

def recommend_movies(user_id, top_k=200):
    if user_id + ID_OFFSET not in user_features_df['user_id'].values:
        print(f"User ID {user_id + ID_OFFSET} vượt quá số lượng người dùng đã được huấn luyện. Sử dụng phương pháp đề xuất cold-start.")
        return cold_start_recommendation(user_id, top_k)

    top_tmdb_ids = []

    model = TwoTowerModel(user_model, movie_model, movie_dataset)
    model.load_weights(os.path.join(ARTIFACTS_PATH, "two_tower_best_weights.weights.h5"))
    print("Đã load trọng số mô hình thành công!")

    all_movie_ids = np.arange(NUM_MOVIES)
    all_movie_vectors = model.movie_model.predict(all_movie_ids, batch_size=4096, verbose=1)
    print("Movies shape:", all_movie_vectors.shape)

    top_k_encoded_ids, top_k_scores = get_top_k_recommendations(model, user_id, all_movie_vectors, k=top_k)
    encoded2real_movie_id = {encoded_val: real_id for real_id, encoded_val in movie2movie_encoded.items()}
    top_tmdb_ids = mapping_movie_id_to_tmdb_id([encoded2real_movie_id[encoded_id] for encoded_id in top_k_encoded_ids])

    if __name__ == "__main__":
        print(f"TOP {top_k} PHIM DÀNH CHO USER {user_id}:")

        for i in range(top_k):
            encoded_id = top_k_encoded_ids[i]
            similarity_score = top_k_scores[i]
            
            # Dịch ngược ID
            real_movie_id = encoded2real_movie_id[encoded_id]
            
            movie_info = movies_df[movies_df['movieId'] == real_movie_id]
            title = movie_info['title'].values[0]
            genres = movie_info['genres'].values[0]
            
            match_percentage = ((similarity_score + 1) / 2) * 100
            
            print(f"{i+1:2d}. {title[:40]:<42} | Độ khớp: {match_percentage:5.1f}% | Thể loại: {genres}")

    return top_tmdb_ids


if __name__ == "__main__":
    target_user_id = 13
    top_recommend = recommend_movies(target_user_id, top_k=10)
    print("\nDanh sách TMDB IDs của các phim được đề xuất:")
    print(top_recommend)
