import streamlit as st
import yfinance as yf
import pandas as pd

# 設置頁面基礎
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 將資料載入改為按鈕觸發，避免頁面載入時無限等待
@st.cache_data(ttl=3600)
def load_stock_data(ticker):
    stock = yf.Ticker(f"{ticker}.TW")
    # 設定 timeout 防止 API 卡死
    hist = stock.history(period="1mo", timeout=10)
    return hist, stock.info

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        with st.spinner('正在分析市場數據...'):
            try:
                df, info = load_stock_data(ticker)
                if df is not None and not df.empty:
                    # 顯示市場動態卡片
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
                    c2.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                    c3.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                    c4.metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                    st.line_chart(df['Close'])
                else:
                    st.error("無法取得數據，請確認代號正確。")
            except Exception as e:
                st.error(f"連線超時或發生錯誤: {e}")
