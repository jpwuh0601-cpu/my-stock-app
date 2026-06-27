import streamlit as st
import pandas as pd
import requests

# 設定網頁標題
st.set_page_config(page_title="股市決策系統", layout="wide")
st.title("📊 專業股市決策系統 (Alpha Vantage API 版)")

# 安全讀取 API 金鑰
try:
    API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]
except:
    API_KEY = "H6Q4KBN202010AV4" 

# 使用 Alpha Vantage 獲取數據的函式
def fetch_stock_data(ticker):
    try:
        # 轉換代號格式，Alpha Vantage 台股需加 TW: 前綴
        symbol = ticker.replace(".TW", "")
        if ".TW" in ticker:
            symbol = f"TW:{symbol}"
        
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 除錯區塊：若沒抓到預期數據，直接在網頁顯示原始回傳內容
        if "Time Series (Daily)" not in data:
            st.error(f"API 回傳異常訊息：{data}")
            return None
            
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.index)
        return df.sort_index(ascending=False)
    except Exception as e:
        st.error(f"發生連線錯誤：{e}")
        return None

# 側邊欄
menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("正在從 Alpha Vantage 取得資料..."):
            df = fetch_stock_data(ticker_input.strip().upper())
            if df is None:
                st.error("無法取得資料，請參考上述 API 回傳的錯誤訊息。")
            else:
                current_price = float(df['Close'].iloc[0])
                st.metric("最新收盤價", f"{round(current_price, 2)}")
                st.write("近期走勢數據 (前 5 筆):")
                st.table(df.head(5))

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
