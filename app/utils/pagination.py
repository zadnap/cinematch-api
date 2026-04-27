def normalize_page(page, max_page=500):
    return min(max(1, page), max_page)