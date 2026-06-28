import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面配置
st.set_page_config(page_title="股市決策系統", layout="wide")

st.title("📈 AI 專業投資決策中樞")

# 側邊欄輸入
ticker_input = st.sidebar.text_input("輸入股票代號 (例如 2330)", "2330")

# 核心：使用快取函數，並設定較短的 timeout，避免無限等待
@st.cache_data(ttl=600)
def fetch_stock_data(ticker):
    try:
        # 加入 timeout 限制網路請求時間
        stock = yf.Ticker(f"{ticker}.TW")
        df = stock.history(period="1mo", timeout=10) 
        info = stock.info
        return df, info
    except Exception as e:
        return None, str(e)

if st.sidebar.button("啟動專業分析"):
    with st.spinner('正在從財經資料庫同步最新市場數據...'):
        df, info = fetch_stock_data(ticker_input)
        
        if df is None:
            st.error(f"數據載入失敗: {info}")
        else:
            # 顯示市場動態
            cols = st.columns(4)
            cols[0].metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
            # 安全獲取 EPS 和本益比 (若 info 抓取失敗則顯示 N/A)
            cols[1].metric("EPS", info.get('trailingEps', 'N/A'))
            cols[2].metric("本益比", info.get('trailingPE', 'N/A'))
            cols[3].metric("每股淨值", info.get('bookValue', 'N/A'))
            
            st.subheader("股價走勢")
            st.line_chart(df['Close'])

else:
    st.info("請於左側輸入代號並點擊「啟動專業分析」以載入數據。")
