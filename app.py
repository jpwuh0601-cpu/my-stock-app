import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (yfinance 穩定版)", layout="wide")
st.title("📊 專業股市決策系統 (yfinance 穩定版)")

st.info("提示：已切換至 yfinance 引擎，連線穩定度大幅提升。請注意台股代號需加上 .TW (例如: 2330.TW)")

# 定義抓取資料函式 (使用 yfinance)
def fetch_stock_data(ticker, days=60):
    try:
        # yfinance 自動處理連線與重試
        stock = yf.Ticker(ticker)
        # 設定較寬鬆的下載逾時，防止雲端逾時導致轉圈
        df = stock.history(period=f"{days}d", timeout=10)
        if not df.empty:
            df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
            return df.sort_index(ascending=False)
        return None
    except Exception as e:
        st.error(f"連線錯誤: {e}")
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
        
        # 使用空容器來即時更新狀態，避免轉圈卡死
        results_container = st.empty()
        
        with st.spinner("正在載入中..."):
            for t in tickers:
                res = fetch_stock_data(t)
                if res is not None:
                    latest = float(res['收盤價'].iloc[0])
                    data_list.append({"代號": t, "最新價": round(latest, 2)})
                else:
                    st.error(f"代號 {t} 載入失敗")
        
        if data_list:
            df_final = pd.DataFrame(data_list)
            st.table(df_final)
            st.success("全部載入完畢！")
