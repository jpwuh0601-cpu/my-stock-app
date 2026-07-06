import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 1. 載入每日自動分析的資料庫
def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

# 2. 處理股票代號格式 (自動處理有無 .TW)
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

# 3. 執行查詢
if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 邏輯 A：如果資料庫裡有這檔股票的預先分析 (從 JSON 讀)
    if ticker in data_cache:
        st.success(f"已載入 {ticker} 的深度分析報告")
        d = data_cache[ticker]
        st.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        st.subheader("法人籌碼分析")
        st.table(pd.DataFrame(d.get("institutional_data", [])))
        st.subheader("AI 深度分析")
        st.info(d.get("ai_prediction", "分析處理中..."))
    
    # 邏輯 B：如果資料庫沒這檔，直接即時向 Yahoo 抓取股價 (補抓功能)
    else:
        with st.spinner(f"正在即時抓取 {ticker} 的股價資訊..."):
            try:
                stock = yf.Ticker(ticker)
                # 簡單抓取股價
                price = stock.info.get("currentPrice") or stock.info.get("regularMarketPrice")
                if price:
                    st.metric("即時股價 (即時抓取)", f"{float(price):.2f}")
                    st.info(f"系統提示：{ticker} 目前未包含在每日自動分析清單中，故無法提供法人籌碼與 AI 深度報告。")
                else:
                    st.error(f"無法取得代號 {ticker} 的股價，請確認代號是否正確。")
            except Exception as e:
                st.error("即時抓取失敗，請確認代號格式是否正確。")

else:
    st.info("請輸入股票代號並點擊「查詢分析數據」。")
