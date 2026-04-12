from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Optional

import feedparser
import requests

from app.models import NewsItem


class RSSCollector:
    def __init__(self, source_name: str, feed_url: str, timeout: int = 10) -> None:
        self.source_name = source_name
        self.feed_url = feed_url
        self.timeout = timeout

    def collect(self, limit: int | None = None) -> List[NewsItem]:
        try:
            response = requests.get(self.feed_url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            print(f"[ERROR] Failed to load RSS '{self.source_name}': {exc}")
            return []

        feed = feedparser.parse(response.content)

        if getattr(feed, "bozo", False):
            print(f"[WARN] RSS '{self.source_name}' may be malformed")

        items: List[NewsItem] = []
        entries = feed.entries[:limit] if limit else feed.entries

        for entry in entries:
            title = self._get_title(entry)
            url = self._get_url(entry)
            published_at = self._get_published_at(entry)
            summary = self._get_summary(entry)

            if not title or not url:
                continue

            items.append(
                NewsItem(
                    title=title,
                    url=url,
                    source=self.source_name,
                    published_at=published_at,
                    summary=summary,
                )
            )

        return items

    @staticmethod
    def _get_title(entry: object) -> str:
        return getattr(entry, "title", "").strip()

    @staticmethod
    def _get_url(entry: object) -> str:
        return getattr(entry, "link", "").strip()

    @staticmethod
    def _get_summary(entry: object) -> str:
        summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
        return summary.strip()

    @staticmethod
    def _get_published_at(entry: object) -> Optional[datetime]:
        raw_date = (
            getattr(entry, "published", None)
            or getattr(entry, "updated", None)
            or getattr(entry, "created", None)
        )

        if not raw_date:
            return None

        try:
            return parsedate_to_datetime(raw_date)
        except (TypeError, ValueError, IndexError):
            return None