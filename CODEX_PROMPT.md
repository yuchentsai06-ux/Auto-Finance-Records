# 給 Codex 的指令

請幫我檢查並完善這個 GitHub repo。這是一個 Daily Economy Notion Bot，目標是每天自動抓取市場數據與財經新聞，使用 OpenAI 整理成繁體中文市場日誌，並寫入 Notion。

請特別檢查：

1. GitHub Actions 是否可以每天台灣時間 08:30 執行。
2. Secrets 是否使用：
   - OPENAI_API_KEY
   - NOTION_TOKEN
   - NOTION_DAILY_DATABASE_ID
   - NOTION_MACRO_DATABASE_ID
3. Notion 欄位是否符合我的 Daily Economy Log：
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
4. Multi-select 欄位格式是否正確。
5. 如果 yfinance 或 RSS 失敗，要保留 fallback。
6. README 是否足夠讓我照著操作。
7. 如果可以，請新增：
   - 每週回顧 workflow
   - 每月回顧 workflow
   - 總經儀表板寫入
   - 財報追蹤寫入
