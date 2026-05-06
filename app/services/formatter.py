from app.models import NewsItem


def format_news_digest(items: list[NewsItem]) -> str:
    if not items:
        return "Новостей по заданным критериям не найдено."

    lines: list[str] = [
        "📰 Tech News Digest",
        "",
    ]

    for index, item in enumerate(items, start=1):
        published = (
            item.published_at.strftime("%Y-%m-%d %H:%M")
            if item.published_at
            else "дата неизвестна"
        )

        lines.extend(
            [
                f"{index}. {item.title}",
                f"Источник: {item.source}",
                f"Дата: {published}",
                f"Score: {item.score}",
                f"Ссылка: {item.url}",
                "",
            ]
        )

    return "\n".join(lines)