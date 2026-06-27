import streamlit as st
import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (極致穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (穩定版)")

# 核心優化：將連線檢查提升至最外層
def fetch_stock_data(ticker, days=60):
    try:
        # 強制極低頻率請求
        time.sleep(2.0)
        url = "https://api.finmindtrade.com/v2/api/data"
        params = {
            "dataset": "TaiwanStockPrice",
            "data_id": ticker,
            "start_date": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params, timeout=5) # 進一步縮短逾時設定
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200 and data.get("data"):
                df = pd.DataFrame(data["data"])
                df = df.rename(columns={"date": "Date", "close": "Close"})
                df["Date"] = pd.to_datetime(df["Date"])
                return df.set_index("Date").sort_index(ascending=False)
        return None
    except:
        return None

menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號", "2330")
    if st.button("查詢分析"):
        data = fetch_stock_data(ticker_input.strip())
        if data is not None:
            st.metric("最新收盤價", round(float(data['Close'].iloc[0]), 2))
            st.table(data.head(5))
        else:
            st.warning("⚠️ 連線受限，請過幾秒後再試，或檢查代號是否正確。")

elif menu == "批量比較":
    st.subheader("⚖️ 批量比較 (建議一次不超過 3 檔)")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330, 2454")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data_list = []
        
        with st.spinner("載入中..."):
            for t in tickers:
                res = fetch_stock_data(t)
                if res is not None:
                    latest = float(res['Close'].iloc[0])
                    data_list.append({"代號": t, "最新價": latest})
                else:
                    st.error(f"代號 {t} 載入失敗 (可能是網路限制)")
        
        if data_list:
            st.table(pd.DataFrame(data_list))
