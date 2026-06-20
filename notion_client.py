from __future__ import annotations

from typing import Any, Dict, List
import requests

NOTION_VERSION = "2022-06-28"

class NotionClient:
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        }

    def _rich_text(self, text: str) -> Dict[str, Any]:
        # Notion rich_text object has a 2000 char limit per text block.
        text = text or ""
        return {"rich_text": [{"type": "text", "text": {"content": text[:1900]}}]}

    def _title(self, text: str) -> Dict[str, Any]:
        return {"title": [{"type": "text", "text": {"content": text[:1900]}}]}

    def _select(self, value: str | None) -> Dict[str, Any]:
        if not value:
            return {"select": None}
        return {"select": {"name": value}}

    def _multi_select(self, values: List[str] | None) -> Dict[str, Any]:
        values = values or []
        return {"multi_select": [{"name": v} for v in values]}

    def _date(self, value: str) -> Dict[str, Any]:
        return {"date": {"start": value}}

    def create_daily_record(self, data_source_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        properties = {
            "紀錄標題": self._title(payload.get("紀錄標題", "每日經濟紀錄")),
            "日期": self._date(payload["日期"]),
            "類型": self._select(payload.get("類型", "每日紀錄")),
            "市場方向": self._select(payload.get("市場方向", "觀望")),
            "重要程度": self._select(payload.get("重要程度", "中")),
            "主要市場": self._multi_select(payload.get("主要市場", [])),
            "產業主題": self._multi_select(payload.get("產業主題", [])),
            "自訂標籤": self._multi_select(payload.get("自訂標籤", [])),
            "股市摘要": self._rich_text(payload.get("股市摘要", "")),
            "總經摘要": self._rich_text(payload.get("總經摘要", "")),
            "新聞重點": self._rich_text(payload.get("新聞重點", "")),
            "新動向/趨勢": self._rich_text(payload.get("新動向/趨勢", "")),
            "關鍵數據": self._rich_text(payload.get("關鍵數據", "")),
            "影響分析": self._rich_text(payload.get("影響分析", "")),
            "觀察清單": self._rich_text(payload.get("觀察清單", "")),
            "可能風險": self._rich_text(payload.get("可能風險", "")),
            "個人想法": self._rich_text(payload.get("個人想法", "")),
            "資料來源": self._rich_text(payload.get("資料來源", "")),
            "Codex狀態": self._select(payload.get("Codex狀態", "已由 Codex 寫入")),
        }

        body = {
            "parent": {"data_source_id": data_source_id},
            "properties": properties,
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "完整市場日誌"}}]},
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": self._compose_page_body(payload)[:1900]}}]},
                },
            ],
        }

        url = f"{self.base_url}/pages"
        resp = requests.post(url, headers=self.headers, json=body, timeout=30)
        if not resp.ok:
            raise RuntimeError(f"Notion create page failed: {resp.status_code} {resp.text}")
        return resp.json()

    def _compose_page_body(self, payload: Dict[str, Any]) -> str:
        sections = [
            ("股市摘要", payload.get("股市摘要", "")),
            ("總經摘要", payload.get("總經摘要", "")),
            ("新聞重點", payload.get("新聞重點", "")),
            ("新動向/趨勢", payload.get("新動向/趨勢", "")),
            ("關鍵數據", payload.get("關鍵數據", "")),
            ("影響分析", payload.get("影響分析", "")),
            ("觀察清單", payload.get("觀察清單", "")),
            ("可能風險", payload.get("可能風險", "")),
            ("個人想法", payload.get("個人想法", "")),
        ]
        return "\n\n".join([f"【{title}】\n{text}" for title, text in sections])
