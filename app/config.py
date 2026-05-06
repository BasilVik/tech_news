import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


def load_env() -> None:
    if not ENV_FILE.exists():
        return

    with ENV_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith("#"):
                continue

            if "=" not in stripped_line:
                continue

            key, value = stripped_line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            os.environ.setdefault(key, value)


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