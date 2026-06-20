from __future__ import annotations

import json
from typing import Any, Dict, List
from openai import OpenAI

ALLOWED_MARKET_DIRECTIONS = ["偏多", "偏空", "震盪", "觀望"]
ALLOWED_IMPORTANCE = ["高", "中", "低"]
ALLOWED_MARKETS = ["台股", "美股", "中國/港股", "日本", "歐洲", "全球", "債券", "外匯", "商品", "加密貨幣"]
ALLOWED_INDUSTRIES = ["AI", "半導體", "電子/硬體", "金融", "能源", "原物料", "消費", "房地產", "生技", "航運", "政策/央行", "地緣政治"]
ALLOWED_CUSTOM_TAGS = [
    "重要新聞", "AI", "半導體", "台股", "美股", "總經", "央行/Fed", "財報",
    "匯率", "債券", "能源", "地緣政治", "待追蹤", "可寫報告", "考試連結"
]

def _filter_allowed(values: Any, allowed: List[str]) -> List[str]:
    if not isinstance(values, list):
        return []
    return [v for v in values if v in allowed]

def _fallback_payload(today: str, reason: str) -> Dict[str, Any]:
    return {
        "紀錄標題": f"{today} 每日經濟紀錄",
        "日期": today,
        "類型": "每日紀錄",
        "市場方向": "觀望",
        "重要程度": "中",
        "主要市場": ["台股", "美股", "全球", "債券", "外匯"],
        "產業主題": ["AI", "半導體", "政策/央行"],
        "自訂標籤": ["待追蹤", "總經"],
        "股市摘要": f"自動摘要失敗，需人工檢查。原因：{reason}",
        "總經摘要": "請人工補充利率、匯率、通膨、央行與債券市場資訊。",
        "新聞重點": "請人工補充 5–8 則重要新聞。",
        "新動向/趨勢": "請人工補充產業與市場趨勢。",
        "關鍵數據": "請人工檢查 yfinance 數據。",
        "影響分析": "請人工補充市場邏輯。",
        "觀察清單": "請人工補充明日與下週觀察重點。",
        "可能風險": "資料來源或模型摘要失敗。",
        "個人想法": "這筆資料需要人工檢查。",
        "資料來源": "yfinance, RSS feeds",
        "Codex狀態": "需人工檢查",
    }

def summarize_daily_report(
    *,
    client: OpenAI,
    model: str,
    today: str,
    market_text: str,
    news_text: str,
) -> Dict[str, Any]:
    system = (
        "你是財金系學生的市場研究助理。"
        "你要根據市場數據與新聞，產生可寫入 Notion 的繁體中文每日經濟紀錄。"
        "請避免空泛評論，每一段要有「數據或事件 → 市場反應 → 可能影響」邏輯。"
        "輸出必須是純 JSON，不要 markdown，不要解釋。"
    )

    user = f"""
今天日期：{today}

市場數據：
{market_text}

新聞資料：
{news_text}

請輸出 JSON，欄位必須完全如下：
{{
  "紀錄標題": "{today} 每日經濟紀錄",
  "日期": "{today}",
  "類型": "每日紀錄",
  "市場方向": "偏多/偏空/震盪/觀望",
  "重要程度": "高/中/低",
  "主要市場": ["台股", "美股", "全球", "債券", "外匯", "商品"],
  "產業主題": ["AI", "半導體", "政策/央行"],
  "自訂標籤": ["重要新聞", "AI", "半導體", "台股", "美股", "總經", "央行/Fed", "待追蹤"],
  "股市摘要": "...",
  "總經摘要": "...",
  "新聞重點": "...",
  "新動向/趨勢": "...",
  "關鍵數據": "...",
  "影響分析": "...",
  "觀察清單": "...",
  "可能風險": "...",
  "個人想法": "...",
  "資料來源": "...",
  "Codex狀態": "已由 Codex 寫入"
}}

限制：
1. 市場方向只能是：偏多、偏空、震盪、觀望。
2. 重要程度只能是：高、中、低。
3. 主要市場只能從這些選：{ALLOWED_MARKETS}
4. 產業主題只能從這些選：{ALLOWED_INDUSTRIES}
5. 自訂標籤只能從這些選：{ALLOWED_CUSTOM_TAGS}
6. 新聞重點請列 5–8 則，每則包含：事件、原因、影響。
7. 個人想法請用財金系學生口吻，連結一個課堂概念，例如利率、匯率、通膨、景氣循環、公司財報或資金流。
"""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        content = resp.choices[0].message.content or "{}"
        payload = json.loads(content)

        payload["紀錄標題"] = str(payload.get("紀錄標題") or f"{today} 每日經濟紀錄")
        payload["日期"] = today
        payload["類型"] = "每日紀錄"
        if payload.get("市場方向") not in ALLOWED_MARKET_DIRECTIONS:
            payload["市場方向"] = "觀望"
        if payload.get("重要程度") not in ALLOWED_IMPORTANCE:
            payload["重要程度"] = "中"

        payload["主要市場"] = _filter_allowed(payload.get("主要市場"), ALLOWED_MARKETS)
        payload["產業主題"] = _filter_allowed(payload.get("產業主題"), ALLOWED_INDUSTRIES)
        payload["自訂標籤"] = _filter_allowed(payload.get("自訂標籤"), ALLOWED_CUSTOM_TAGS)

        if not payload["主要市場"]:
            payload["主要市場"] = ["台股", "美股", "全球"]
        if not payload["產業主題"]:
            payload["產業主題"] = ["政策/央行"]
        if not payload["自訂標籤"]:
            payload["自訂標籤"] = ["待追蹤"]

        payload["Codex狀態"] = "已由 Codex 寫入"
        return payload
    except Exception as exc:
        return _fallback_payload(today, str(exc))
