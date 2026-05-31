# query_templates.py
# ambiguous Query and intent-based
# also some queries that could map to multiple genres, to create real ambiguity
import random

# ── Intent-based queries ─────────────────────────────────
#each genre → multiple ambiguous queries that don't directly say the genre - this is intentional to create ambiguity and make the task more realistic
GENRE_TO_QUERIES = {
    "Action": [
        "I want something exciting and fast-paced",
        "I need an adrenaline rush tonight",
        "I want something energetic to watch",
    ],
    "Adventure": [
        "I want to go on a journey without leaving my couch",
        "I feel like escaping somewhere new",
        "I want something epic and sweeping",
    ],
    "Animation": [
        "I want something visually stunning",
        "I feel like watching something imaginative",
        "I want a movie that feels like a different world",
    ],
    "Children's": [
        "I want something wholesome and fun",
        "I need something the whole family can enjoy",
        "I want something light and innocent",
    ],
    "Comedy": [
        "I had a rough day and just want to laugh",
        "I want something easy and fun to watch",
        "I need something to lift my mood",
    ],
    "Crime": [
        "I want something gritty and real",
        "I feel like watching something dark and urban",
        "I want a story about the darker side of society",
    ],
    "Documentary": [
        "I want to learn something tonight",
        "I want something thought-provoking and real",
        "I'm in the mood for something factual",
    ],
    "Drama": [
        "I want something emotionally deep",
        "I'm in the mood for a meaningful story",
        "I want something that makes me feel something",
    ],
    "Fantasy": [
        "I want to escape reality completely",
        "I feel like something magical tonight",
        "I want a world that doesn't exist",
    ],
    "Film-Noir": [
        "I want something dark and atmospheric",
        "I'm in the mood for something moody and mysterious",
        "I want a story with shadows and secrets",
    ],
    "Horror": [
        "I want something that scares me",
        "I'm in the mood for something unsettling",
        "I want a movie that keeps me up at night",
    ],
    "Musical": [
        "I want something uplifting with great music",
        "I feel like something joyful and energetic",
        "I want a movie that makes me want to sing",
    ],
    "Mystery": [
        "I want something that keeps me guessing",
        "I love not knowing what happens next",
        "I want a puzzle to solve while watching",
    ],
    "Romance": [
        "I want something that warms my heart",
        "I'm in the mood for a love story",
        "I want something emotional and tender",
    ],
    "Sci-Fi": [
        "I want something mind-bending tonight",
        "I feel like exploring the future",
        "I want something that makes me question reality",
    ],
    "Thriller": [
        "I want to stay on the edge of my seat",
        "I need something intense and gripping",
        "I want something I can't stop watching",
    ],
    "War": [
        "I want something powerful and intense",
        "I want a story about human struggle",
        "I'm in the mood for something serious and impactful",
    ],
    "Western": [
        "I want something rugged and classic",
        "I feel like watching an old-fashioned story",
        "I want something with wide open spaces and tension",
    ],
}

# ── Multi-genre intent queries ───────────────────────────
# a query that could map to multiple genres — real ambiguity
COMBO_TO_QUERIES = {
    "Action|Adventure": [
        "I want something big and exciting",
        "I feel like an epic adventure tonight",
    ],
    "Action|Thriller": [
        "I want something intense that doesn't let up",
        "I need a gripping high-stakes movie",
    ],
    "Comedy|Romance": [
        "I want something fun and heartwarming",
        "I want a feel-good movie for tonight",
    ],
    "Drama|Romance": [
        "I want something emotional and touching",
        "I want a story about love and loss",
    ],
    "Animation|Children's|Comedy": [
        "I want something fun for the whole family",
        "I need something cheerful and light",
    ],
    "Crime|Thriller": [
        "I want a dark and suspenseful story",
        "I want something morally complex",
    ],
    "Horror|Thriller": [
        "I want something genuinely frightening",
        "I want to feel uneasy the whole time",
    ],
    "Drama|War": [
        "I want something powerful and heavy",
        "I want a film that stays with me",
    ],
    "Sci-Fi|Thriller": [
        "I want something paranoid and futuristic",
        "I want a film that messes with my head",
    ],
    "Comedy|Drama": [
        "I want something that makes me laugh and cry",
        "I want something real but not too heavy",
    ],
}


def get_query_for_movie(genres_str: str, random_pick: bool = True) -> str:
    """
    genres_str like 'Animation|Children's|Comedy'
    random_pick=True 
    means pick a random query from the possible ones, 
    False means always pick the first one (for deterministic testing)
    """
    # exact match روی combo
    if genres_str in COMBO_TO_QUERIES:
        queries = COMBO_TO_QUERIES[genres_str]
        return random.choice(queries) if random_pick else queries[0]

    # partial match روی combo
    movie_genres = set(genres_str.split('|'))
    best_queries = None
    best_overlap = 0
    for combo, queries in COMBO_TO_QUERIES.items():
        overlap = len(movie_genres & set(combo.split('|')))
        if overlap > best_overlap:
            best_overlap = overlap
            best_queries = queries

    if best_queries and best_overlap >= 2:
        return random.choice(best_queries) if random_pick else best_queries[0]

    # single genre fallback
    for genre in genres_str.split('|'):
        if genre in GENRE_TO_QUERIES:
            queries = GENRE_TO_QUERIES[genre]
            return random.choice(queries) if random_pick else queries[0]

    return "I'm looking for something good to watch tonight"


if __name__ == '__main__':
    random.seed(42)
    test_cases = [
        "Animation|Children's|Comedy",
        "Action|Thriller",
        "Drama|Romance",
        "Horror",
        "Crime|Drama|Thriller",
        "Sci-Fi",
        "Comedy",
    ]
    print('Genre → Ambiguous Query:')
    print()
    for g in test_cases:
        print(f'  {g:35s}')
        print(f'  → "{get_query_for_movie(g)}"')
        print()
