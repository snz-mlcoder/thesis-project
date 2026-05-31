# query_templates_amazon.py
# ambiguous Query and intent-based for Amazon Clothing/Shoes/Jewelry
# not directly based on category- using mood/occasion/intent 
#ambiguous queries based on category keywords, with some occasion-based fallbacks for more ambiguity
import random

# ── Category → ambiguous queries ────────────────────────
CATEGORY_TO_QUERIES = {
    # Clothing
    "Dresses": [
        "I need something to wear to a special occasion",
        "I want to look nice for an event",
        "I'm looking for something elegant to wear out",
    ],
    "Casual": [
        "I want something comfortable for everyday wear",
        "I need something relaxed and easy to wear",
        "I'm looking for something simple and comfortable",
    ],
    "T-Shirts": [
        "I need something basic to wear around the house",
        "I want something simple and comfortable",
        "I'm looking for everyday basics",
    ],
    "Blouses": [
        "I need something professional to wear to work",
        "I want to look put-together without being too formal",
        "I'm looking for something smart-casual",
    ],
    "Tunics": [
        "I want something loose and comfortable",
        "I need something that works for both casual and semi-formal",
        "I'm looking for something flowy and relaxed",
    ],
    "Skirts": [
        "I want something feminine to wear out",
        "I need something versatile for different occasions",
        "I'm looking for a fun and stylish bottom",
    ],
    "Jeans": [
        "I need a reliable pair of bottoms for everyday use",
        "I want something casual and durable",
        "I'm looking for something I can wear anywhere",
    ],
    "Swimsuits": [
        "I'm going to the beach and need something to wear",
        "I want something stylish for a pool day",
        "I need something for a summer vacation",
    ],
    "Cover-Ups": [
        "I need something light to wear over my swimsuit",
        "I want a stylish layer for a beach day",
        "I'm looking for something breezy for summer",
    ],
    "Activewear": [
        "I need something to work out in",
        "I want comfortable clothes for the gym",
        "I'm looking for athletic wear",
    ],
    "Running": [
        "I need something for my morning runs",
        "I want gear for outdoor exercise",
        "I'm looking for performance sportswear",
    ],
    "Lingerie": [
        "I need something comfortable for everyday wear underneath",
        "I'm looking for something that fits well and feels good",
        "I want something practical and comfortable",
    ],
    "Bras": [
        "I need comfortable everyday support",
        "I'm looking for something that fits perfectly",
        "I want something practical for daily use",
    ],

    # Shoes
    "Shoes": [
        "I need a new pair of shoes",
        "I'm looking for something comfortable to walk in",
        "I want shoes that go with everything",
    ],
    "Sandals": [
        "I want something open and breezy for warm weather",
        "I need comfortable shoes for summer",
        "I'm looking for easy slip-on shoes",
    ],
    "Flats": [
        "I want comfortable shoes that still look nice",
        "I need something I can walk in all day",
        "I'm looking for practical yet stylish shoes",
    ],
    "Pumps": [
        "I need shoes for a formal occasion",
        "I want to look polished and professional",
        "I'm looking for elegant shoes for an event",
    ],
    "Sneakers": [
        "I want something casual and comfortable to walk around in",
        "I need everyday shoes that are easy to wear",
        "I'm looking for stylish yet practical footwear",
    ],
    "Hiking": [
        "I need shoes for outdoor activities",
        "I'm going on a trail and need proper footwear",
        "I want durable shoes for nature walks",
    ],
    "Boots": [
        "I need shoes for colder weather",
        "I want something sturdy and stylish",
        "I'm looking for boots I can wear in fall and winter",
    ],

    # Bags & Accessories
    "Handbags": [
        "I need a bag for going out",
        "I want something stylish to carry my things in",
        "I'm looking for a new everyday bag",
    ],
    "Crossbody Bags": [
        "I need a hands-free bag for travel",
        "I want something practical and stylish",
        "I'm looking for a bag I can wear all day",
    ],
    "Wallets": [
        "I need something to organize my cards and cash",
        "I want a compact and practical wallet",
        "I'm looking for a slim everyday wallet",
    ],
    "Jewelry": [
        "I need an accessory to complete my outfit",
        "I want something elegant to wear",
        "I'm looking for a nice piece of jewelry",
    ],
    "Watches": [
        "I want something stylish for my wrist",
        "I need an accessory that works for everyday wear",
        "I'm looking for a watch that goes with everything",
    ],

    # Generic fallbacks
    "Women": [
        "I'm looking for something stylish for women",
        "I want a nice women's clothing item",
        "I need something fashionable to wear",
    ],
    "Men": [
        "I'm looking for something casual for men",
        "I want a practical men's clothing item",
        "I need something comfortable and stylish for men",
    ],
    "Gift": [
        "I want to buy a gift for someone special",
        "I'm looking for something nice as a present",
        "I need a thoughtful gift for a friend",
    ],
}

# ── Occasion-based queries (for more ambiguity) ────────
OCCASION_QUERIES = [
    "I have a wedding coming up and need something to wear",
    "I need an outfit for a job interview",
    "I want something casual for a weekend trip",
    "I'm going on a date and need to look good",
    "I need comfortable clothes for working from home",
    "I want a gift for my wife's birthday",
    "I need something for a beach vacation",
    "I'm looking for workout clothes",
    "I want something warm for winter",
    "I need shoes that go with everything",
]


def get_query_for_item(category_str: str, random_pick: bool = True) -> str:
    """
    category_str like 'Clothing > Dresses > Casual'
    finds the last keyword and returns an appropriate query.
    """
    parts = [p.strip() for p in category_str.replace('>', '/').split('/')]

    # check from last to first to find the most specific match
    for part in reversed(parts):
        for key, queries in CATEGORY_TO_QUERIES.items():
            if key.lower() in part.lower():
                return random.choice(queries) if random_pick else queries[0]

    # fallback: occasion-based query
    return random.choice(OCCASION_QUERIES) if random_pick else OCCASION_QUERIES[0]


if __name__ == '__main__':
    random.seed(42)
    test_cases = [
        "Clothing > Dresses > Casual",
        "Shoes > Sandals > Flats",
        "Women > Handbags & Wallets > Crossbody Bags",
        "Athletic > Running > Road Running",
        "Clothing > Tops, Tees & Blouses > T-Shirts",
        "Lingerie > Bras > Everyday Bras",
    ]
    print('Category → Ambiguous Query:')
    print()
    for c in test_cases:
        print(f'  {c}')
        print(f'  → "{get_query_for_item(c)}"')
        print()
