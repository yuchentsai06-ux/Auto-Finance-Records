# Daily Economy Notion Bot

這是一個可以放到 GitHub Actions 每天自動執行的 Python 專案，用來抓取市場數據與財經新聞，整理成繁體中文「每日經濟紀錄」，並寫入你的 Notion database。

## 功能

- 抓取市場數據：
  - 台股加權指數
  - S&P 500
  - Nasdaq
  - Dow Jones
  - Russell 2000
  - 費半
  - NVIDIA、TSMC、AMD、Microsoft、Meta、Amazon、Google、Apple、Tesla
  - US 10Y、DXY、VIX、WTI Oil、Gold、USD/TWD
- 抓取財經新聞 RSS
- 使用 OpenAI 整理成市場日誌
- 寫入 Notion「每日經濟紀錄」
- 支援 Notion multi-select 標籤欄位：`自訂標籤`
- GitHub Actions 每天自動排程

## Notion database 欄位

主要寫入：

- 紀錄標題
- 日期
- 類型
- 市場方向
- 重要程度
- 主要市場
- 產業主題
- 自訂標籤
- 股市摘要
- 總經摘要
- 新聞重點
- 新動向/趨勢
- 關鍵數據
- 影響分析
- 觀察清單
- 可能風險
- 個人想法
- 資料來源
- Codex狀態

## 1. 建立 Notion Integration

1. 到 https://www.notion.so/my-integrations
2. New integration
3. 複製 Internal Integration Token
4. 到你的 Notion database 頁面
5. 右上角 Share / Connect
6. 加入你的 integration

## 2. GitHub Secrets 設定

到 GitHub repo：

`Settings → Secrets and variables → Actions → New repository secret`

新增：

```txt
OPENAI_API_KEY
NOTION_TOKEN
NOTION_DAILY_DATABASE_ID
NOTION_MACRO_DATABASE_ID
```

你的 Notion Daily database ID：

```txt
f93b0487-d5a9-4ed6-81ef-1450e7c3b5cb
```

你的 Macro Dashboard database ID：

```txt
bc474511-d566-41bd-a6ea-314fbf90a93f
```

## 3. GitHub Actions 排程

檔案位置：

```txt
.github/workflows/daily.yml
```

預設排程：

- UTC 00:30
- 台灣時間 08:30

也可以手動執行：

`Actions → Daily Economy Notion Bot → Run workflow`

## 4. 本機測試

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python src/main.py
```

## 5. 給 Codex 的修改指令

你可以在 Codex 貼：

```txt
請閱讀這個 repo，幫我檢查 daily economy notion bot 是否可以每天抓市場數據、新聞，使用 OpenAI 摘要，並寫入 Notion。請特別確認 Notion 欄位名稱、多選欄位格式、GitHub Actions secrets、錯誤處理與 README 是否完整。如果有問題請直接修改。
```

## 注意

這個專案使用免費資料源，例如 yfinance 與 RSS。新聞與股價資料可能有延遲，不適合作為即時交易依據，適合作為學習、研究與每日市場紀錄。
