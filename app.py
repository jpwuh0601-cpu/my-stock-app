import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

# 1. 自由輸入代號
raw_ticker = st.sidebar.text_input("請輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

# 2. 查詢邏輯
if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 優先從每日分析過的 JSON 撈取 (包含 AI 分析結果)
    if ticker in data_cache:
        st.success(f"已從每日分析庫中讀取 {ticker} 的深度資料")
        d = data_cache[ticker]
        st.metric("即時股價", f"{float(d.get('price', 0)):.2f}")
        st.table(pd.DataFrame(d.get("institutional_data", [])))
        st.info(d.get("ai_prediction", "分析處理中..."))
    
    # 若 JSON 沒有，強制啟動 API 即時查詢 (不受限於任何清單)
    else:
        st.warning(f"資料庫暫無 {ticker} 的深度分析，啟動即時股價查詢...")
        try:
            stock = yf.Ticker(ticker)
            price = stock.info.get("currentPrice") or stock.info.get("regularMarketPrice")
            if price:
                st.metric("即時股價 (即時抓取)", f"{float(price):.2f}")
                st.info("註：該股票未在每日自動分析任務中，若需詳細籌碼分析，請將其加入每日任務清單。")
            else:
                st.error("無法取得該代號資訊，請檢查代號是否正確。")
        except Exception as e:
            st.error(f"無法即時抓取: {str(e)}")
