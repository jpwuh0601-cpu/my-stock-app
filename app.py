import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

st.title("📈 AI 專業投資決策中樞")

# 1. 將數據獲取邏輯封裝並設定 Timeout
@st.cache_data(ttl=3600) # 快取數據，減少重複請求
def get_stock_data(ticker):
    stock = yf.Ticker(f"{ticker}.TW")
    # 設定 timeout 避免 API 沒回應導致卡死
    hist = stock.history(period="1mo", timeout=5) 
    return hist, stock.info

# 2. UI 設計
t = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("載入數據"):
    try:
        with st.spinner('正在從雅虎財經獲取數據...'):
            hist, info = get_stock_data(t)
            
            if hist.empty:
                st.error("無法取得該股票資料，請檢查代號。")
            else:
                st.metric("最新成交價", f"{hist['Close'].iloc[-1]:.2f}")
                st.line_chart(hist['Close'], width=0) # 修正舊版警告，這會自動適應容器
    except Exception as e:
        st.error(f"連線超時或發生錯誤: {e}")
else:
    st.info("請在側邊欄輸入代號並點擊「載入數據」以開始分析。")
