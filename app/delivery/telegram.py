import json
import os
import urllib.error
import urllib.parse
import urllib.request


TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def send_to_telegram(text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        raise RuntimeError("Environment variable TELEGRAM_BOT_TOKEN is not set")

    if not chat_id:
        raise RuntimeError("Environment variable TELEGRAM_CHAT_ID is not set")

    payload = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        TELEGRAM_API_URL.format(token=token),
        data=payload,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            response_body = response.read().decode("utf-8")
            response_data = json.loads(response_body)

            if response.status != 200 or not response_data.get("ok"):
                raise RuntimeError(
                    f"Telegram API returned unexpected response: {response_body}"
                )

            print("Telegram message sent successfully")

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")
        raise RuntimeError(
            f"Telegram API returned HTTP {error.code}: {error_body}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(f"Failed to connect to Telegram API: {error}") from error
