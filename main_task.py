import json
import os
from worker import fetch_stock_data

def run_main():
    # 簡化任務，僅執行單純的資料獲取
    # ... (您的其他邏輯)
    pass

if __name__ == "__main__":
    run_main()
```

### 2. 簡化版的 `app.py` (手動輸入、直接查詢)
這個版本不再讀取 `market_data.json`，而是直接當您輸入代號時，呼叫 `worker.py` 進行即時查詢。

```python:app.py:app.py
import streamlit as st
from worker import fetch_stock_data

st.set_page_config(page_title="股市即時查詢", layout="centered")

st.title("🔍 股票即時查詢")

# 1. 手動輸入股票代號
ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

if st.button("查詢股價"):
    with st.spinner("正在讀取即時數據..."):
        # 2. 直接查詢
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error(f"查詢失敗: {data['error']}")
        else:
            # 3. 顯示結果
            st.metric("即時股價", f"{data.get('price', 0)} 元")
            st.write(f"本益比 (PE): {data.get('pe', 'N/A')}")
            st.write(f"EPS: {data.get('eps', 'N/A')}")
            st.write(f"每股淨值 (NAV): {data.get('nav', 'N/A')}")
```

### 3. 確保 `worker.py` 穩定
確保您的 `worker.py` 內容如下（維持它之前的偽裝 Header 機制）：

```python:worker.py:worker.py
import yfinance as yf
import requests

def fetch_stock_data(ticker):
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and ticker.isdigit():
        ticker += ".TW"
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        stock = yf.Ticker(ticker, session=session)
        info = stock.info
        
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0
        if price == 0:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                
        return {
            "price": round(price, 2),
            "nav": info.get("bookValue", "N/A"),
            "pe": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
            "eps": round(info.get("trailingEps", 0), 2) if info.get("trailingEps") else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}
```

### 為什麼這樣能解決？
1.  **解決 GitHub Actions 錯誤**：刪除 `main_task.py` 中不存在的 `import` 函式，Action 就能順利通過。
2.  **徹底擺脫檔案讀取卡頓**：不再依賴背景生成的 JSON 檔案，網頁直接查詢即時資料，減少複雜度。
3.  **手動查詢**：使用者體驗更直接，輸入完按查詢即可看到結果。

請將以上內容更新到您的檔案中，並執行 GitHub Action，網頁錯誤應會排除。
