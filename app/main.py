from __future__ import annotations

import os
import sys

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.pipeline import get_top_news
from app.services.formatter import format_news_digest


def main() -> None:
    top_items = get_top_news(limit=10, per_source_limit=25)
    digest = format_news_digest(top_items)
    print(digest)


if __name__ == "__main__":
    main()