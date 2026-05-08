import numpy as np
import pandas as pd
import os
from ml.models.two_towers_model import (
    TwoTowerModel, user_model, movie_model
)

from ml.training.dataset_loader import (
    NUM_MOVIES, 
    movie_dataset,
    interactions
)

from ml.training.data_preprocessing import (
    movie2movie_encoded, movies_df
)

ARTIFACTS_PATH = "ml/artifacts"
PROCESSED_DATA_PATH = "ml/data/processed_data"
RAW_DATA_PATH = "ml/data/raw_data"

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


def recommend_movies(user_id, top_k=200):
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
