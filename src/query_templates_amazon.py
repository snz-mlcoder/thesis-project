"""
Query templates for Amazon product classification.

Defines intent-based queries for various product categories with ambiguous questions,
plus multi-category combinations for testing hybrid recommendations.
"""

CATEGORY_QUERIES = {
    "electronics": [
        "Is this a device or electronic gadget?",
        "Does it require batteries or a power source?",
        "Is this used for computing or digital processing?",
    ],
    "books": [
        "Is this a physical book or written publication?",
        "Is it educational or informational in nature?",
        "Would you read this for entertainment or learning?",
    ],
    "clothing": [
        "Is this a wearable item of apparel?",
        "Is it designed for a specific season or weather?",
        "Is this casual wear or formal attire?",
    ],
    "furniture": [
        "Is this a piece of home or office furniture?",
        "Would you place this indoors for functional use?",
        "Is this designed for sitting, lying, or storage?",
    ],
    "sports": [
        "Is this item related to physical activity or sports?",
        "Would you use this for exercise or athletic training?",
        "Is this sports equipment or workout gear?",
    ],
    "toys": [
        "Is this designed for children to play with?",
        "Is it primarily for entertainment rather than functionality?",
        "Would you classify this as a toy or game?",
    ],
    "beauty": [
        "Is this a cosmetic or personal care product?",
        "Would you use this for skincare or grooming?",
        "Is this related to beauty, wellness, or hygiene?",
    ],
    "home": [
        "Is this designed for home décor or improvement?",
        "Would you use this inside your living space?",
        "Is this for organizing or beautifying your home?",
    ],
    "kitchen": [
        "Is this a kitchen appliance or cooking tool?",
        "Would you use this for food preparation?",
        "Is this related to cooking, baking, or dining?",
    ],
    "garden": [
        "Is this for outdoor gardening or landscaping?",
        "Would you use this to grow plants or flowers?",
        "Is this gardening equipment or outdoor tool?",
    ],
    "automotive": [
        "Is this related to cars or vehicle maintenance?",
        "Would you use this in or on your vehicle?",
        "Is this automotive parts or car accessories?",
    ],
    "pet": [
        "Is this product for pets or animals?",
        "Would you use this to care for a pet?",
        "Is this pet food, toys, or pet accessories?",
    ],
    "office": [
        "Is this for office work or professional use?",
        "Would you use this at a desk or workspace?",
        "Is this office supplies or equipment?",
    ],
    "music": [
        "Is this related to music or audio?",
        "Would you use this to listen to or create music?",
        "Is this a musical instrument or audio equipment?",
    ],
    "health": [
        "Is this related to health or medical care?",
        "Would you use this for fitness or wellness?",
        "Is this health supplements or medical equipment?",
    ],
    "outdoor": [
        "Is this for outdoor activities or camping?",
        "Would you use this outside or in nature?",
        "Is this camping, hiking, or outdoor gear?",
    ],
    "photography": [
        "Is this related to photography or image capture?",
        "Would you use this to take photos or videos?",
        "Is this photography equipment or camera accessories?",
    ],
    "luggage": [
        "Is this for travel or storage on the go?",
        "Would you use this to carry items while traveling?",
        "Is this luggage, bags, or travel accessories?",
    ],
}

# Multi-category combinations for testing
MULTI_CATEGORY_QUERIES = [
    ("electronics", "sports", "Is this an electronic sports device or fitness tracker?"),
    ("beauty", "health", "Is this a beauty or health/wellness product?"),
    ("home", "kitchen", "Is this for the kitchen or home decoration?"),
    ("books", "education", "Is this an educational or learning resource?"),
    ("toys", "games", "Is this a toy or board game?"),
    ("office", "electronics", "Is this electronic office equipment?"),
    ("outdoor", "sports", "Is this outdoor sports or camping gear?"),
    ("pet", "toys", "Is this a pet toy or pet accessory?"),
    ("automotive", "tools", "Is this an automotive tool or car maintenance item?"),
    ("music", "electronics", "Is this an electronic musical device?"),
]

# Helper function to get a random query
def get_query(category: str) -> str:
    """Get a query for a specific category."""
    if category not in CATEGORY_QUERIES:
        raise ValueError(f"Unknown category: {category}")
    return CATEGORY_QUERIES[category][0]  # Return first query


def get_all_queries(category: str) -> list:
    """Get all queries for a specific category."""
    if category not in CATEGORY_QUERIES:
        raise ValueError(f"Unknown category: {category}")
    return CATEGORY_QUERIES[category]


def get_multi_category_query(category1: str, category2: str) -> str:
    """Get a query for a combination of two categories."""
    for c1, c2, query in MULTI_CATEGORY_QUERIES:
        if (c1 == category1 and c2 == category2) or (c1 == category2 and c2 == category1):
            return query
    raise ValueError(f"Unknown category combination: {category1}, {category2}")


if __name__ == "__main__":
    print("Amazon Product Category Queries")
    print("=" * 60)
    
    for category, queries in CATEGORY_QUERIES.items():
        print(f"\n🛍️  {category.upper()}")
        for i, query in enumerate(queries, 1):
            print(f"   {i}. {query}")
    
    print("\n\n" + "=" * 60)
    print("Multi-Category Combinations")
    print("=" * 60)
    
    for category1, category2, query in MULTI_CATEGORY_QUERIES:
        print(f"\n{category1.upper()} + {category2.upper()}")
        print(f"  {query}")
