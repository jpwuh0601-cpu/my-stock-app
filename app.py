import streamlit as st
import pandas as pd
import requests

# 設定網頁標題
st.set_page_config(page_title="股市決策系統", layout="wide")
st.title("📊 專業股市決策系統 (Alpha Vantage API 版)")

# 安全讀取 API 金鑰
# 請確保在 Streamlit Cloud 的 Secrets 設定: ALPHA_VANTAGE_API_KEY = "H6Q4KBN202010AV4"
try:
    API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]
except:
    API_KEY = "" # 移除預設硬編碼，強制使用 Secrets

# 使用 Alpha Vantage 獲取數據的函式
@st.cache_data(ttl=3600) # 加入快取，每小時更新一次，避免重複請求
def fetch_stock_data(ticker):
    try:
        # 針對台股格式處理：Alpha Vantage 需要特定後綴
        # 若用戶輸入 2330，嘗試自動補上 .TW
        symbol = ticker.strip().upper()
        if not any(ext in symbol for ext in [".TW", ".HK", ".US"]):
            symbol = f"{symbol}.TW"
        
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            df.index = pd.to_datetime(df.index)
            return df.sort_index(ascending=False)
        return None
    except Exception as e:
        return None

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入股票代號 (例如 2330)", "2330")
    if st.button("查詢分析"):
        if not API_KEY:
            st.error("請在 Streamlit Cloud 設定中補上 ALPHA_VANTAGE_API_KEY")
        else:
            with st.spinner("正在查詢..."):
                df = fetch_stock_data(ticker_input)
                if df is not None:
                    current_price = float(df['Close'].iloc[0])
                    st.metric("最新收盤價", f"{round(current_price, 2)}")
                    st.table(df.head(5))
                else:
                    st.error("無法取得資料，請確認代號是否支援 (台股請嘗試輸入含 .TW 的代號)。")

elif menu == "批量比較":
    st.subheader("⚖️ 股票數據批量比較")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip().upper() for t in tickers_input.split(",")]
        data = []
        for t in tickers:
            df = fetch_stock_data(t)
            if df is not None:
                data.append({"代號": t, "最新價": round(float(df['Close'].iloc[0]), 2)})
            else:
                data.append({"代號": t, "最新價": "抓取失敗"})
        if data:
            st.table(pd.DataFrame(data))
