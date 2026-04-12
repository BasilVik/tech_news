from __future__ import annotations

from app.models import NewsItem
from app.services.pipeline import get_top_news


def print_news(items: list[NewsItem]) -> None:
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item.title}")
        print(f"   Source: {item.source}")
        print(f"   URL: {item.url}")
        print(f"   Published: {item.published_at}")
        print(f"   Score: {item.score}")
        print()


def main() -> None:
    top_items = get_top_news(limit=10, per_source_limit=25)
    print_news(top_items)


if __name__ == "__main__":
    main()