import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 將資料載入改為延遲處理
@st.cache_data(ttl=3600)
def fetch_data(ticker):
    try:
        # 使用 yfinance 穩定抓取
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="1mo")
        return hist, stock.info
    except Exception:
        return None, None

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 確保不會自動執行請求
    ticker = st.text_input("輸入股票代號", "2330")
    
    if st.button("載入資料"):
        with st.spinner("連線中..."):
            hist, info = fetch_data(ticker)
            if hist is not None and not hist.empty:
                st.success(f"成功載入 {ticker}")
                # 顯示數據卡片
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("股價", f"{hist['Close'].iloc[-1]:.2f}")
                c2.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                c3.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                c4.metric("淨值", f"{info.get('bookValue', 0):.2f}")
                st.line_chart(hist['Close'])
            else:
                st.error("無法載入資料，請檢查代號。")

elif menu == "部位管理":
    st.title("💼 部位管理")
    st.write("系統建置中。")
