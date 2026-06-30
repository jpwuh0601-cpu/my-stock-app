import streamlit as st
import json
import os
import yfinance as yf
import pandas as pd
import time

# 設定頁面配置
st.set_page_config(page_title="即時投資決策儀表板", layout="wide")

st.title("📊 即時投資決策儀表板")

# 使用快取來避免觸發 Rate Limit
@st.cache_data(ttl=300) # 快取 5 分鐘
def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    # 增加 delay 以降低被封鎖風險
    time.sleep(1)
    hist = ticker.history(period="1d")
    return hist

# 讀取數據的函式
def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取數據檔錯誤: {e}")
    return None

# 側邊欄查詢
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

# 加入「開始搜尋」按鈕，解決輸入即觸發導致轉圈圈的問題
search_button = st.sidebar.button("開始搜尋")

if search_button and ticker_input:
    ticker_symbol = f"{ticker_input}.TW"
    
    try:
        # 使用狀態顯示避免轉圈圈時無反應
        with st.spinner(f"正在查詢 {ticker_input} 的即時股價..."):
            hist = get_stock_data(ticker_symbol)
        
        if hist is None or hist.empty:
            st.error(f"無法取得 {ticker_symbol} 的資料，請確認代碼是否正確。")
        else:
            current_price = hist['Close'].iloc[-1]
            st.subheader(f"代碼: {ticker_input} 最新價格: {current_price:.2f}")
            
            # 嘗試讀取本地 JSON 數據作為補充資訊
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
            else:
                st.warning("目前沒有 AI 分析數據可顯示。")
            
    except Exception as e:
        st.error(f"系統發生錯誤: {str(e)}")
elif search_button and not ticker_input:
    st.sidebar.warning("請先輸入股票代碼！")
else:
    st.write("請在左側輸入代碼並點選「開始搜尋」按鈕。")

# 顯示最後更新時間
if os.path.exists("market_data.json"):
    st.sidebar.markdown(f"---")
    last_mod = os.path.getmtime('market_data.json')
    st.sidebar.caption(f"數據最後更新於: {pd.to_datetime(last_mod, unit='s')}")
