from __future__ import annotations

import json
from datetime import datetime
import pytz
from openai import OpenAI

from config import get_settings
from market_data import fetch_market_snapshot, format_market_snapshot
from news_fetcher import fetch_news, format_news
from summarizer import summarize_daily_report
from notion_client import NotionClient

def main() -> None:
    settings = get_settings()
    tz = pytz.timezone(settings.timezone)
    today = datetime.now(tz).strftime("%Y-%m-%d")

    print(f"Running daily economy bot for {today}")

    market_snapshot = fetch_market_snapshot()
    market_text = format_market_snapshot(market_snapshot)
    print("Fetched market data")

    news_items = fetch_news(max_items=30)
    news_text = format_news(news_items)
    print(f"Fetched {len(news_items)} news items")

    openai_client = OpenAI(api_key=settings.openai_api_key)
    payload = summarize_daily_report(
        client=openai_client,
        model=settings.openai_model,
        today=today,
        market_text=market_text,
        news_text=news_text,
    )

    # Store local debug artifact for GitHub Actions logs if needed.
    with open("daily_payload.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    notion = NotionClient(settings.notion_token)
    created = notion.create_daily_record(settings.notion_daily_database_id, payload)
    print("Created Notion page:")
    print(created.get("url"))

if __name__ == "__main__":
    main()
