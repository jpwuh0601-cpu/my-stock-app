import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (yfinance 穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (yfinance 穩定版)")

st.info("提示：已啟用自動重試機制，連線穩定度大幅提升。請注意台股代號需加上 .TW (例如: 2330.TW)")

# 定義抓取資料函式 (使用 yfinance)
def fetch_stock_data(ticker, days=60):
    # 增加重試機制，應對雲端偶發瞬斷
    for attempt in range(2):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=f"{days}d", timeout=15)
            
            if df is not None and not df.empty:
                df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
                return df.sort_index(ascending=False)
            
            # 若無資料，休息一下再試
            time.sleep(1)
        except Exception:
            time.sleep(1)
            continue
    return None

menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號 (需加 .TW)", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("正在讀取資料..."):
            data = fetch_stock_data(ticker_input.strip())
            if data is not None:
                st.metric("最新收盤價", f"{round(float(data['收盤價'].iloc[0]), 2)}")
                st.table(data.head(5))
            else:
                st.warning("⚠️ 無法獲取資料，請檢查代號是否正確。")

elif menu == "批量比較":
    st.subheader("⚖️ 批量比較 (請輸入 .TW 代號)")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data_list = []
        
        with st.spinner("正在載入中，請耐心等候..."):
            for t in tickers:
                res = fetch_stock_data(t)
                if res is not None:
                    latest = float(res['收盤價'].iloc[0])
                    data_list.append({"代號": t, "最新價": round(latest, 2), "狀態": "成功"})
                else:
                    data_list.append({"代號": t, "最新價": "-", "狀態": "連線失敗"})
                
        if data_list:
            df_final = pd.DataFrame(data_list)
            st.table(df_final)
            st.success("批量載入處理完畢！")
