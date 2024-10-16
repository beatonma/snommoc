from fuzzywuzzy import fuzz


def get_similarity_score(a, b):
    return fuzz.token_sort_ratio(a, b)
