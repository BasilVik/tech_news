from __future__ import annotations

from datetime import datetime

from app.collectors.rss import RSSCollector
from app.config import RSS_SOURCES, BLACKLIST_KEYWORDS, KEYWORD_BOOSTS
from app.models import NewsItem


# --- Этап 1: сбор данных ---

def collect_all_rss_news(per_source_limit: int = 25) -> list[NewsItem]:
    all_items: list[NewsItem] = []

    for source in RSS_SOURCES:
        collector = RSSCollector(
            source_name=source["source_name"],
            feed_url=source["feed_url"],
        )

        items = collector.collect(limit=per_source_limit)
        print(f"[INFO] Collected {len(items)} items from {source['source_name']}")
        all_items.extend(items)

    return all_items


# --- Этап 2: фильтрация мусора ---

def filter_noise(items: list[NewsItem]) -> list[NewsItem]:
    filtered_items: list[NewsItem] = []

    for item in items:
        text = f"{item.title} {item.summary}".lower()

        if any(keyword in text for keyword in BLACKLIST_KEYWORDS):
            continue

        filtered_items.append(item)

    return filtered_items


# --- Этап 3: дедупликация ---

def deduplicate_news(items: list[NewsItem]) -> list[NewsItem]:
    unique_items: list[NewsItem] = []
    seen_urls: set[str] = set()

    for item in items:
        normalized_url = item.url.strip().lower()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_items.append(item)

    return unique_items


# --- Этап 4: скоринг ---

def score_news_item(item: NewsItem) -> float:
    score = 0.0
    text = f"{item.title} {item.summary}".lower()

    # базовый сигнал: есть дата
    if item.published_at is not None:
        score += 1

    # ключевые слова
    for keyword, boost in KEYWORD_BOOSTS.items():
        if keyword in text:
            score += boost

    # бонус за источник
    if item.source == "Hacker News":
        score += 1

    return score


def rank_news(items: list[NewsItem]) -> list[NewsItem]:
    ranked_items: list[NewsItem] = []

    for item in items:
        item.score = score_news_item(item)
        ranked_items.append(item)

    return sorted(
        ranked_items,
        key=lambda item: (item.score, item.published_at or datetime.min),
        reverse=True,
    )


# --- Запуск конвейера ---

def run_pipeline(per_source_limit: int = 25) -> list[NewsItem]:
    """
    Полный конвейер обработки новостей.
    Возвращает отсортированный список (но не обрезает top-N).
    """
    raw_items = collect_all_rss_news(per_source_limit=per_source_limit)
    filtered_items = filter_noise(raw_items)
    unique_items = deduplicate_news(filtered_items)
    ranked_items = rank_news(unique_items)

    return ranked_items


# --- Получить top-N новостей ---

def get_top_news(limit: int = 10, per_source_limit: int = 25) -> list[NewsItem]:
    ranked_items = run_pipeline(per_source_limit=per_source_limit)
    return ranked_items[:limit]