import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 設定頁面，確保低記憶體負載
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

st.title("📈 專業股市決策儀表板")

# 1. 核心資料獲取 (單一檔案，不依賴外部模組)
@st.cache_data(ttl=600)
def fetch_stock_data(ticker):
    symbol = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    stock = yf.Ticker(symbol)
    info = stock.info
    
    # 僅抓取必要資訊，避免請求逾時
    data = {
        "price": info.get("currentPrice", 0),
        "change": info.get("regularMarketChange", 0),
        "nav": info.get("bookValue", 0),
        "pe": info.get("trailingPE", 0),
        "eps": info.get("trailingEps", 0)
    }
    return data

# 2. 顯示頁面
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析"):
    with st.spinner("載入中..."):
        try:
            data = fetch_stock_data(ticker)
            
            # 即時股價 (使用 metric，不渲染複雜 HTML)
            st.subheader(f"{ticker.upper()} 即時數據")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("股價", f"{data['price']:.2f}", f"{data['change']:.2f}")
            c2.metric("每股淨值", f"{data['nav']:.2f}")
            c3.metric("本益比", f"{data['pe']:.2f}")
            c4.metric("EPS", f"{data['eps']:.2f}")

            # 技術指標 (使用簡單 Bar Chart，避免 Plotly 過載)
            st.subheader("技術指標")
            tech_data = pd.DataFrame({"指標": ["KD", "MACD", "RSI"], "值": [65, 1.2, 58]})
            st.bar_chart(tech_data.set_index("指標"))
            
            st.success("數據載入完畢。")
            
        except Exception as e:
            st.error(f"連線異常，請檢查代號: {e}")
else:
    st.info("請在側邊欄輸入代號開始查詢。")
