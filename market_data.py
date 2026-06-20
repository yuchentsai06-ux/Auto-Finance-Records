from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import yfinance as yf

TICKERS = {
    "台股加權指數": "^TWII",
    "櫃買指數": "^TWOII",
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT",
    "費半": "^SOX",
    "NVIDIA": "NVDA",
    "TSMC ADR": "TSM",
    "AMD": "AMD",
    "Microsoft": "MSFT",
    "Meta": "META",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "台積電": "2330.TW",
    "鴻海": "2317.TW",
    "聯發科": "2454.TW",
    "廣達": "2382.TW",
    "緯創": "3231.TW",
    "US 10Y Yield": "^TNX",
    "DXY": "DX-Y.NYB",
    "VIX": "^VIX",
    "WTI Oil": "CL=F",
    "Gold": "GC=F",
    "USD/TWD": "TWD=X",
}

def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None

def fetch_market_snapshot() -> Dict[str, Dict[str, Any]]:
    """
    Fetch latest market data with yfinance.
    Returns a compact dict that is easy to send to OpenAI.
    """
    result: Dict[str, Dict[str, Any]] = {}

    for name, ticker in TICKERS.items():
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="5d", interval="1d", auto_adjust=False)
            if hist.empty:
                result[name] = {"ticker": ticker, "error": "no data"}
                continue

            last = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) >= 2 else None

            close = _safe_float(last.get("Close"))
            prev_close = _safe_float(prev.get("Close")) if prev is not None else None
            change = None
            change_pct = None
            if close is not None and prev_close not in (None, 0):
                change = close - prev_close
                change_pct = (change / prev_close) * 100

            result[name] = {
                "ticker": ticker,
                "close": round(close, 4) if close is not None else None,
                "change": round(change, 4) if change is not None else None,
                "change_pct": round(change_pct, 2) if change_pct is not None else None,
                "volume": int(last.get("Volume")) if "Volume" in last and not str(last.get("Volume")) == "nan" else None,
            }
        except Exception as exc:
            result[name] = {"ticker": ticker, "error": str(exc)}

    return result

def format_market_snapshot(snapshot: Dict[str, Dict[str, Any]]) -> str:
    lines = []
    for name, item in snapshot.items():
        if "error" in item:
            lines.append(f"{name} ({item.get('ticker')}): ERROR {item['error']}")
            continue
        lines.append(
            f"{name} ({item.get('ticker')}): close={item.get('close')}, "
            f"change={item.get('change')}, change_pct={item.get('change_pct')}%, "
            f"volume={item.get('volume')}"
        )
    return "\n".join(lines)
