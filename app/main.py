from __future__ import annotations

from datetime import datetime
from typing import List

from app.collectors.rss import RSSCollector
from app.config import RSS_SOURCES
from app.models import NewsItem


def collect_all_rss_news(per_source_limit: int = 25) -> List[NewsItem]:
    all_items: List[NewsItem] = []

    for source in RSS_SOURCES:
        collector = RSSCollector(
            source_name=source["source_name"],
            feed_url=source["feed_url"],
        )

        items = collector.collect(limit=per_source_limit)
        print(f"[INFO] Collected {len(items)} items from {source['source_name']}")
        all_items.extend(items)

    return all_items


def deduplicate_news(items: List[NewsItem]) -> List[NewsItem]:
    unique_items: List[NewsItem] = []
    seen_urls: set[str] = set()

    for item in items:
        normalized_url = item.url.strip().lower()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_items.append(item)

    return unique_items


def sort_news(items: List[NewsItem]) -> List[NewsItem]:
    return sorted(
        items,
        key=lambda item: item.published_at or datetime.min,
        reverse=True,
    )


def get_top_news(limit: int = 10, per_source_limit: int = 25) -> List[NewsItem]:
    raw_items = collect_all_rss_news(per_source_limit=per_source_limit)
    unique_items = deduplicate_news(raw_items)
    sorted_items = sort_news(unique_items)
    return sorted_items[:limit]


def print_news(items: List[NewsItem]) -> None:
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item.title}")
        print(f"   Source: {item.source}")
        print(f"   URL: {item.url}")
        print(f"   Published: {item.published_at}")
        print()


def main() -> None:
    top_items = get_top_news(limit=10, per_source_limit=25)
    print_news(top_items)


if __name__ == "__main__":
    main()