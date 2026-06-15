# catalog.py
# Shared product catalog used by both the homepage and the support chatbot.

PRODUCTS = [
    {
        "id": "MS001",
        "name": "AeroBuds Pro",
        "price": 79.99,
        "description": "Wireless earbuds with active noise cancellation, 24-hour battery life, and crystal-clear call quality.",
        "category": "Electronics",
        "icon": "🎧",
    },
    {
        "id": "MS002",
        "name": "PulseFit Smart Watch",
        "price": 129.00,
        "description": "Fitness-focused smartwatch with heart-rate tracking, sleep monitoring, and 7-day battery life.",
        "category": "Wearables",
        "icon": "⌚",
    },
    {
        "id": "MS003",
        "name": "UrbanLite Backpack",
        "price": 54.50,
        "description": "Minimalist water-resistant backpack with padded laptop sleeve and hidden anti-theft pocket.",
        "category": "Accessories",
        "icon": "🎒",
    },
    {
        "id": "MS004",
        "name": "SoundSphere Mini Speaker",
        "price": 45.99,
        "description": "Portable Bluetooth speaker with rich bass, 12-hour playtime, and splash-resistant design.",
        "category": "Electronics",
        "icon": "🔊",
    },
    {
        "id": "MS005",
        "name": "BrewCraft Mug Set",
        "price": 32.00,
        "description": "Set of 4 ceramic coffee mugs with matte finish, stackable design, and dishwasher-safe coating.",
        "category": "Home",
        "icon": "☕",
    },
    {
        "id": "MS006",
        "name": "FlexDesk Laptop Stand",
        "price": 39.90,
        "description": "Ergonomic aluminum laptop stand with adjustable height and foldable travel-friendly design.",
        "category": "Office",
        "icon": "💻",
    },
]

CATEGORIES = ["All"] + sorted({product["category"] for product in PRODUCTS})


def get_product_by_id(product_id: str):
    """Return a product dictionary by its ID."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def get_catalog_text() -> str:
    """Build a clean text catalog for the OpenAI system prompt."""
    lines = []
    for product in PRODUCTS:
        lines.append(
            f"- {product['name']} ({product['category']}) - ${product['price']:.2f}: {product['description']}"
        )
    return "\n".join(lines)
