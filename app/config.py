RSS_SOURCES = [
    {
        "source_name": "Hacker News",
        "feed_url": "https://news.ycombinator.com/rss",
    },
    {
        "source_name": "TechCrunch",
        "feed_url": "https://techcrunch.com/feed/",
    },
    {
        "source_name": "Ars Technica",
        "feed_url": "https://feeds.arstechnica.com/arstechnica/index",
    },
]

# --- Настройки фильтрации и скоринга ---

BLACKLIST_KEYWORDS = {
    "sponsored",
    "webinar",
    "podcast",
    "video",
    "promo",
    "advertisement",
}


KEYWORD_BOOSTS = {
    "ai": 3,
    "llm": 3,
    "agent": 2,
    "agents": 2,
    "security": 2,
    "database": 2,
    "architecture": 2,
    "engineering": 2,
    "programming": 1,
}