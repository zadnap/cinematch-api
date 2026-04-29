import numpy as np
import os

ARTIFACTS_PATH = "ml/artifacts"

_user_embeddings = None
_movie_embeddings = None
_movie_ids = None

def load_artifacts():
    global _user_embeddings, _movie_embeddings, _movie_ids

    if _user_embeddings is None:
        _user_embeddings = np.load(os.path.join(ARTIFACTS_PATH, "user_embeddings.npy"))
        _movie_embeddings = np.load(os.path.join(ARTIFACTS_PATH, "movie_embeddings.npy"))
        _movie_ids = np.load(os.path.join(ARTIFACTS_PATH, "movie_ids.npy"))


def recommend_movies(user_id, top_k=200):
    load_artifacts()
    top_tmdb_ids = []

    return top_tmdb_ids