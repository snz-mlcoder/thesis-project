"""
Query templates for movie genre classification.

Defines intent-based queries for 18 movie genres with 3 ambiguous questions each,
plus 10 multi-genre combinations for testing hybrid recommendations.
"""

GENRE_QUERIES = {
    "action": [
        "Does this movie feature intense fight scenes?",
        "Is there a lot of explosions and physical combat?",
        "Does it have high-speed chases or dangerous stunts?",
    ],
    "comedy": [
        "Is this movie designed to make you laugh?",
        "Does it rely on jokes and humorous situations?",
        "Would you watch this movie to have a good laugh?",
    ],
    "drama": [
        "Does this movie focus on emotional storytelling?",
        "Are the characters dealing with serious life problems?",
        "Is the plot centered on human relationships and conflicts?",
    ],
    "horror": [
        "Is this movie designed to scare the audience?",
        "Does it feature frightening creatures or supernatural elements?",
        "Would you describe this as a suspenseful thriller?",
    ],
    "romance": [
        "Is love and relationships the main focus?",
        "Does it feature a romantic relationship as the central plot?",
        "Would you classify this as a love story?",
    ],
    "sci-fi": [
        "Does this movie involve futuristic technology?",
        "Are there space, aliens, or advanced scientific concepts?",
        "Is the story set in an alternate reality or future world?",
    ],
    "thriller": [
        "Is this movie designed to keep you on the edge of your seat?",
        "Does it involve suspense and unexpected plot twists?",
        "Is there a sense of danger or mystery throughout?",
    ],
    "animation": [
        "Is this movie made using animation techniques?",
        "Are the characters drawn or computer-generated?",
        "Is this intended for children or family viewing?",
    ],
    "adventure": [
        "Does the story involve exploration or journeys?",
        "Are the characters going on exciting quests?",
        "Does it feature outdoor activities or exotic locations?",
    ],
    "crime": [
        "Does this movie involve illegal activities or investigations?",
        "Is it centered around detectives, criminals, or law enforcement?",
        "Does the plot revolve around solving a mystery or heist?",
    ],
    "fantasy": [
        "Does this movie feature magical elements or mythical creatures?",
        "Is the story set in an imaginary world with magic?",
        "Are there wizards, dragons, or enchanted objects?",
    ],
    "history": [
        "Is this movie set in a historical time period?",
        "Does it tell the story of real historical events?",
        "Are the characters based on real historical figures?",
    ],
    "musical": [
        "Are songs and musical performances central to the movie?",
        "Do characters frequently burst into song?",
        "Is this a movie where music drives the narrative?",
    ],
    "mystery": [
        "Does the plot involve solving a puzzle or secret?",
        "Are you trying to figure out who did something?",
        "Is there a gradual revelation of hidden information?",
    ],
    "western": [
        "Is this movie set in the American Old West?",
        "Does it feature cowboys, outlaws, or frontier life?",
        "Are there gunfights and desert landscapes?",
    ],
    "sport": [
        "Is this movie centered around sports competition?",
        "Does it feature athletes training and competing?",
        "Is the main plot about winning a championship or competition?",
    ],
    "family": [
        "Is this movie suitable for all ages?",
        "Would you watch this with children?",
        "Does it contain family-friendly humor and values?",
    ],
    "documentary": [
        "Is this a factual film about real events or people?",
        "Is it designed to inform and educate?",
        "Does it feature real footage and interviews?",
    ],
}

# Multi-genre combinations for testing
MULTI_GENRE_QUERIES = [
    ("action", "sci-fi", "Does this movie combine futuristic tech with intense action?"),
    ("comedy", "romance", "Is this a romantic comedy?"),
    ("drama", "crime", "Does this movie combine serious drama with crime investigation?"),
    ("horror", "thriller", "Is this a suspenseful horror film?"),
    ("adventure", "fantasy", "Does this movie feature fantasy worlds and epic journeys?"),
    ("animation", "comedy", "Is this an animated comedy?"),
    ("action", "adventure", "Does this movie have action sequences and adventure elements?"),
    ("drama", "history", "Is this a historical drama based on real events?"),
    ("musical", "comedy", "Is this a comedic musical?"),
    ("mystery", "crime", "Does this involve mystery and crime investigation?"),
]

# Helper function to get a random query
def get_query(genre: str) -> str:
    """Get a query for a specific genre."""
    if genre not in GENRE_QUERIES:
        raise ValueError(f"Unknown genre: {genre}")
    return GENRE_QUERIES[genre][0]  # Return first query


def get_all_queries(genre: str) -> list:
    """Get all queries for a specific genre."""
    if genre not in GENRE_QUERIES:
        raise ValueError(f"Unknown genre: {genre}")
    return GENRE_QUERIES[genre]


def get_multi_genre_query(genre1: str, genre2: str) -> str:
    """Get a query for a combination of two genres."""
    for g1, g2, query in MULTI_GENRE_QUERIES:
        if (g1 == genre1 and g2 == genre2) or (g1 == genre2 and g2 == genre1):
            return query
    raise ValueError(f"Unknown genre combination: {genre1}, {genre2}")


if __name__ == "__main__":
    print("Movie Genre Queries")
    print("=" * 60)
    
    for genre, queries in GENRE_QUERIES.items():
        print(f"\n📽️  {genre.upper()}")
        for i, query in enumerate(queries, 1):
            print(f"   {i}. {query}")
    
    print("\n\n" + "=" * 60)
    print("Multi-Genre Combinations")
    print("=" * 60)
    
    for genre1, genre2, query in MULTI_GENRE_QUERIES:
        print(f"\n{genre1.upper()} + {genre2.upper()}")
        print(f"  {query}")
