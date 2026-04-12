from app.collectors.rss import RSSCollector


def main() -> None:
    collector = RSSCollector(
        source_name="Hacker News RSS",
        feed_url="https://news.ycombinator.com/rss",
    )

    items = collector.collect()

    for index, item in enumerate(items[:10], start=1):
        print(f"{index}. {item.title}")
        print(f"   Source: {item.source}")
        print(f"   URL: {item.url}")
        print(f"   Published: {item.published_at}")
        print()


if __name__ == "__main__":
    main()