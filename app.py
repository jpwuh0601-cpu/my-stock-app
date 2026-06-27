import streamlit as st
import requests
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (穩定 API 版)", layout="wide")
st.title("📊 專業股市決策系統 (Alpha Vantage API)")

# 從 Secrets 安全讀取 API Key
try:
    API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]
except:
    API_KEY = "demo" # 若未設定則使用 demo 金鑰 (僅支援 IBM)

# 定義抓取資料函式 (使用 requests 直接存取，最穩定)
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    try:
        # 為了避開 cloud 環境網路阻塞，使用 requests 直連
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            df.index = pd.to_datetime(df.index)
            return df.sort_index(ascending=False)
        elif "Note" in data:
            return "limit" # 代表 API 限額已滿
        else:
            return "empty"
    except Exception as e:
        return str(e)

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    st.info("提示：輸入代號 (例如 IBM, AAPL) - 若使用免費金鑰，請以查詢 IBM 為主")
    ticker_input = st.text_input("輸入股票代號", "IBM")
    if st.button("查詢分析"):
        with st.spinner("正在讀取資料..."):
            result = fetch_stock_data(ticker_input.strip().upper())
            if isinstance(result, pd.DataFrame):
                current_price = float(result['Close'].iloc[0])
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                st.table(result.head(5))
            elif result == "limit":
                st.warning("API 請求次數已達上限，請稍後再試。")
            elif result == "empty":
                st.error("查無資料，請確認代號是否支援。")
            else:
                st.error(f"系統錯誤: {result}")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "IBM, AAPL")
    if st.button("開始比較"):
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        data = []
        for t in tickers:
            result = fetch_stock_data(t)
            if isinstance(result, pd.DataFrame):
                data.append({"代號": t, "最新價": round(float(result['Close'].iloc[0]), 2)})
            else:
                data.append({"代號": t, "最新價": "失敗"})
        if data:
            st.table(pd.DataFrame(data))
