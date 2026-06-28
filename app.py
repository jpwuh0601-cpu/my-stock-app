import streamlit as st
import yfinance as yf
import pandas as pd

# 設置頁面基礎
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 強制將數據處理與 UI 邏輯解耦
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    try:
        # yfinance 請求加入異常捕捉
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="1mo", timeout=10)
        return hist, stock.info
    except Exception:
        return None, None

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 使用 Form 提交，這能保證網頁渲染不被 API 請求阻塞
    with st.form("stock_data_fetcher"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner("正在載入財經數據..."):
            hist, info = fetch_stock_data(ticker)
            if hist is not None and not hist.empty:
                st.success("數據載入成功")
                cols = st.columns(4)
                cols[0].metric("股價", f"{hist['Close'].iloc[-1]:.2f}")
                cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                cols[3].metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                st.line_chart(hist['Close'])
            else:
                st.error("無法連線至財經資料庫，請稍後再試。")

elif menu == "部位管理":
    st.title("💼 部位管理系統")
    st.write("系統功能建置中，此頁面已正常掛載。")
