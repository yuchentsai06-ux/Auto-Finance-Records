from __future__ import annotations

from typing import List, Dict
import feedparser
import time

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.reuters.com/reuters/marketsNews",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
    "https://finance.yahoo.com/news/rssindex",
    "https://www.ft.com/markets?format=rss",
]

KEYWORDS = [
    "stock", "market", "Fed", "rate", "inflation", "CPI", "PCE", "jobs",
    "AI", "semiconductor", "Nvidia", "TSMC", "Taiwan", "China", "oil",
    "bond", "yield", "dollar", "earnings", "tech"
]

def fetch_news(max_items: int = 30) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []

    for feed_url in RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
            source = parsed.feed.get("title", feed_url)
            for entry in parsed.entries[:15]:
                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()
                link = entry.get("link", "")
                published = entry.get("published", "")

                text = f"{title} {summary}".lower()
                if KEYWORDS and not any(k.lower() in text for k in KEYWORDS):
                    continue

                items.append({
                    "source": source,
                    "title": title,
                    "summary": summary[:600],
                    "link": link,
                    "published": published,
                })
        except Exception:
            continue

        time.sleep(0.2)

    # Deduplicate by title
    seen = set()
    deduped: List[Dict[str, str]] = []
    for item in items:
        title_key = item["title"].lower()
        if title_key in seen:
            continue
        seen.add(title_key)
        deduped.append(item)

    return deduped[:max_items]

def format_news(items: List[Dict[str, str]]) -> str:
    lines = []
    for i, item in enumerate(items, start=1):
        lines.append(
            f"{i}. [{item.get('source')}] {item.get('title')}\n"
            f"   published: {item.get('published')}\n"
            f"   summary: {item.get('summary')}\n"
            f"   link: {item.get('link')}"
        )
    return "\n".join(lines)
