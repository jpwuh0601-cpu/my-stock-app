import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# 設定網頁標題
st.set_page_config(page_title="股市決策系統 (yfinance 高穩版)", layout="wide")
st.title("📊 專業股市決策系統 (yfinance 高穩版)")

st.info("提示：已啟用強化的重試機制與錯誤處理。")

# 定義抓取資料函式
def fetch_stock_data(ticker, days=60):
    """使用重試機制獲取股票資料"""
    # 設置重試參數
    max_retries = 3
    for attempt in range(max_retries):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # 建立 ticker 對象並嘗試獲取資料
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date, timeout=20)
            
            if not df.empty:
                # 處理可能的 MultiIndex
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                df = df.rename(columns={"Close": "收盤價", "Open": "開盤價", "High": "最高價", "Low": "最低價", "Volume": "成交量"})
                return df.sort_index(ascending=False)
            
            # 若為空但無報錯，休息後重試
            time.sleep(2 * (attempt + 1))
            
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"連線多次失敗，請稍後重試。代號: {ticker}")
                return None
            time.sleep(3) # 失敗後等待較長時間
    return None

menu = st.sidebar.radio("功能選單", ["個股分析", "批量比較"])

if menu == "個股分析":
    ticker_input = st.text_input("輸入台股代號 (需加 .TW)", "2330.TW")
    if st.button("查詢分析"):
        with st.spinner("正在讀取資料..."):
            data = fetch_stock_data(ticker_input.strip())
            if data is not None and not data.empty:
                try:
                    latest = float(data['收盤價'].iloc[0])
                    st.metric("最新收盤價", f"{round(latest, 2)}")
                    st.table(data.head(5))
                except:
                    st.warning("資料格式異常。")
            else:
                st.warning("⚠️ 無法獲取資料，可能是網路環境受限，請稍後重試。")

elif menu == "批量比較":
    st.subheader("⚖️ 批量比較 (請輸入 .TW 代號)")
    tickers_input = st.text_input("輸入代號 (逗號分隔)", "2330.TW, 2454.TW")
    if st.button("開始比較"):
        tickers = [t.strip() for t in tickers_input.split(",")]
        data_list = []
        
        with st.spinner("載入中..."):
            for t in tickers:
                res = fetch_stock_data(t)
                if res is not None and not res.empty:
                    latest = float(res['收盤價'].iloc[0])
                    data_list.append({"代號": t, "最新價": round(latest, 2), "狀態": "成功"})
                else:
                    data_list.append({"代號": t, "最新價": "-", "狀態": "失敗"})
                
        if data_list:
            df_final = pd.DataFrame(data_list)
            st.table(df_final)
            st.success("處理完畢！")
