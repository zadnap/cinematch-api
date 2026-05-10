import os
import pandas as pd
import re

PROCESSED_DATA_PATH = "ml/data/processed_data"
RAW_DATA_PATH = "ml/data/raw_data"

def extract_year(title):
    match = re.search(r'\((\d{4})\)', title)
    if match:
        return int(match.group(1))
    return None

def export_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Đã xuất file: {filename}")

movies_df = pd.read_csv(os.path.join(RAW_DATA_PATH, "movies.csv"))
ratings_df = pd.read_csv(os.path.join(RAW_DATA_PATH, "ratings.csv"))
movie2movie_encoded = {x: i for i, x in enumerate(movies_df['movieId'].unique())}

if __name__ == "__main__":
    # Map User ID
    user_ids = ratings_df['userId'].unique()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    ratings_df['user_id'] = ratings_df['userId'].map(user2user_encoded)

    # Map Movie ID
    movie_ids = movies_df['movieId'].unique()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movies_df['movie_id'] = movies_df['movieId'].map(movie2movie_encoded)
    ratings_df['movie_id'] = ratings_df['movieId'].map(movie2movie_encoded)

    # Loại bỏ ratings cho những phim không có trong file movies.csv
    ratings_df = ratings_df.dropna(subset=['movie_id'])
    ratings_df['movie_id'] = ratings_df['movie_id'].astype(int)

    print(user_ids.shape)
    print(movie_ids.shape)
    print(ratings_df.shape)

    # One-hot encoding cho genres
    genres_dummies = movies_df['genres'].str.get_dummies(sep='|')
    genres_dummies.drop(columns=['(no genres listed)'], inplace=True)
    genres_dummies.columns = [col.lower().replace('-', '_').replace(' ', '_') for col in genres_dummies.columns]

    movies_df['year'] = movies_df['title'].apply(extract_year)

    # Fill NaN cho year bằng mean của 2 phim trên nó và 2 phim dưới nó
    movies_df['year'] = movies_df['year'].fillna(
        movies_df['year'].rolling(window=5, center=True, min_periods=1).mean()
    ).astype(int)

    movie_features = pd.concat([movies_df[['movie_id']], movies_df[['year']], genres_dummies], axis=1)
    export_to_csv(movie_features, os.path.join(PROCESSED_DATA_PATH, "movie_features.csv"))

    merged_df = pd.merge(ratings_df[['user_id', 'movie_id', 'rating']], movie_features, on='movie_id')
    user_features = pd.DataFrame({'user_id': ratings_df['user_id'].unique()})

    # year_mean_series = merged_df.groupby('user_id')['year'].mean()
    # user_features['year_avg'] = user_features['user_id'].map(year_mean_series).fillna(0.0)

    # Tính điểm trung bình cho từng thể loại
    for genre in genres_dummies.columns:
        genre_ratings = merged_df['rating'].where(merged_df[genre] == 1)
        mean_series = genre_ratings.groupby(merged_df['user_id']).mean()
        avg_col_name = genre + '_avg'
        user_features[avg_col_name] = user_features['user_id'].map(mean_series).fillna(0.0)

    export_to_csv(user_features, os.path.join(PROCESSED_DATA_PATH, "user_features.csv"))

    # Chỉ giữ lại những lượt đánh giá có điểm > 4 từ bảng ratings.csv
    positive_interactions = ratings_df[ratings_df['rating'] > 4]
    # Giữ lại đúng 3 feature cần thiết: user_id, movie_id, và timestamp
    positive_interactions = positive_interactions[['user_id', 'movie_id', 'timestamp']]

    export_to_csv(positive_interactions, os.path.join(PROCESSED_DATA_PATH, "positive_interactions.csv"))