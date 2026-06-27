import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (FinMind 台股版)", layout="wide")
st.title("📊 專業股市決策系統 (FinMind API)")

# 提示用戶 FinMind 使用說明
st.info("提示：FinMind 專為台股設計，請直接輸入代號 (例如: 2330, 2454)")

# 定義抓取資料函式 (使用 FinMind API)
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    try:
        # FinMind API 獲取股價資料
        url = "https://api.finmindtrade.com/v2/api/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": ticker,
            "start_date": (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        if data.get("status") == 200 and data.get("data"):
            df = pd.DataFrame(data["data"])
            # 標準化欄位名稱以符合後續邏輯
            df = df.rename(columns={"date": "Date", "open": "Open", "max": "High", "min": "Low", "close": "Close", "Trading_Volume": "Volume"})
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date").sort_index(ascending=False)
            return df[["Open", "High", "Low", "Close", "Volume"]]
        else:
            return "empty"
    except Exception as e:
        return str(e)

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號", "2330")
    if st.button("查詢分析"):
        with st.spinner("正在讀取 FinMind 台股資料..."):
            result = fetch_stock_data(ticker_input.strip())
            if isinstance(result, pd.DataFrame):
                current_price = float(result['Close'].iloc[0])
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                st.table(result.head(5))
            elif result == "empty":
                st.error("查無資料，請確認代號是否正確。")
            else:
                st.error(f"系統錯誤: {result}")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330, 2454, 2317")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data = []
        success_count = 0
        
        with st.spinner("正在進行批量運算..."):
            for t in tickers:
                result = fetch_stock_data(t)
                if isinstance(result, pd.DataFrame):
                    data.append({"代號": t, "最新價": round(float(result['Close'].iloc[0]), 2)})
                    success_count += 1
                else:
                    data.append({"代號": t, "最新價": "查詢失敗"})
        
        if data:
            st.table(pd.DataFrame(data))
            st.success(f"比較完成！成功獲取 {success_count} 筆，失敗 {len(tickers) - success_count} 筆。")
