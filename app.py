import streamlit as st
import json
import os
import yfinance as yf
import pandas as pd
import time

# 設定頁面配置
st.set_page_config(page_title="即時投資決策儀表板", layout="wide")

st.title("📊 即時投資決策儀表板")

# 增強的快取機制，確保在雲端環境穩定執行
@st.cache_data(ttl=600)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # 增加連線參數，解決部分環境下的網路逾時問題
        hist = ticker.history(period="1d", timeout=5)
        return hist
    except Exception as e:
        return None

# 讀取本地數據
def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

# 側邊欄查詢
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")
search_button = st.sidebar.button("開始搜尋")

if search_button and ticker_input:
    # 確保代碼格式正確
    ticker_symbol = f"{ticker_input}.TW"
    
    with st.spinner("正在連線至市場資料庫..."):
        hist = get_stock_data(ticker_symbol)
        
        if hist is None or hist.empty:
            st.error(f"無法取得 {ticker_symbol} 的資料，請稍後再試。這通常是因為連線限制，請避免頻繁查詢。")
        else:
            current_price = hist['Close'].iloc[-1]
            st.subheader(f"代碼: {ticker_input} 最新價格: {current_price:.2f}")
            
            data = load_market_data()
            if data:
                st.write("---")
                st.write("### AI 智能分析")
                st.info(data.get("ai_prediction", "暫無分析數據"))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("預估 EPS", data.get("est_eps", "N/A"))
                with col2:
                    st.metric("預估股利", data.get("est_dividend", "N/A"))
            
elif search_button and not ticker_input:
    st.sidebar.warning("請先輸入代碼！")
else:
    st.write("請在左側輸入代碼並點選「開始搜尋」。")

if os.path.exists("market_data.json"):
    st.sidebar.markdown("---")
    st.sidebar.caption("數據更新成功。")
