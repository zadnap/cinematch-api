def rerank_movies(movies, rec_ids):
    if not rec_ids:
        return movies

    rank_map = {mid: i for i, mid in enumerate(rec_ids)}

    matched = [m for m in movies if m["id"] in rank_map]
    unmatched = [m for m in movies if m["id"] not in rank_map]

    matched_sorted = sorted(matched, key=lambda m: rank_map[m["id"]])

    return matched_sorted + unmatched