import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import time

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (優化穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (優化穩定版)")

st.info("提示：已移除對 pandas_datareader 的依賴，改用原生的 yfinance 下載機制。")

# 使用 st.cache_data 來儲存資料
@st.cache_data(ttl=3600)
def fetch_stock_data_native(ticker, days=60):
    try:
        # 下載資料
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 使用 yf.download 下載
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if not df.empty:
            # 處理 MultiIndex 欄位 (yfinance 特性)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
            return df.sort_index(ascending=False)
        return None
    except Exception as e:
        return None

menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號 (需加 .TW)", "2330.TW")
    if st.button("查詢分析"):
        data = fetch_stock_data_native(ticker_input.strip())
        if data is not None and not data.empty:
            latest = float(data['收盤價'].iloc[0])
            st.metric("最新收盤價", f"{round(latest, 2)}")
            st.table(data.head(5))
        else:
            st.warning("⚠️ 無法獲取資料，請檢查代號是否正確。")

elif menu == "批量比較":
    st.subheader("⚖️ 批量比較 (請輸入 .TW 代號)")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data_list = []
        
        for t in tickers:
            res = fetch_stock_data_native(t)
            if res is not None and not res.empty:
                latest = float(res['收盤價'].iloc[0])
                data_list.append({"代號": t, "最新價": round(latest, 2)})
            else:
                data_list.append({"代號": t, "最新價": "獲取失敗"})
                
        if data_list:
            st.table(pd.DataFrame(data_list))
