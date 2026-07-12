import streamlit as st
import os
import sys
import pkg_resources

# 強制設定頁面
st.set_page_config(page_title="股市儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 除錯模式：顯示目前 Python 環境安裝的套件
def show_installed_packages():
    st.sidebar.write("### 系統已安裝套件檢查")
    packages = [p.key for p in pkg_resources.working_set]
    if 'yfinance' not in packages:
        st.sidebar.error("❌ 系統偵測到未安裝 yfinance！")
    else:
        st.sidebar.success("✅ yfinance 已安裝")
    st.sidebar.write(f"Python: {sys.version}")

show_installed_packages()

# 核心功能
try:
    import yfinance as yf
    
    ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "").strip().upper()
    if ticker_input:
        with st.spinner("正在查詢..."):
            stock = yf.Ticker(ticker_input)
            info = stock.info
            if "currentPrice" in info:
                st.metric("即時股價", info["currentPrice"])
            else:
                st.error("查無此代號")
except ImportError:
    st.error("系統嚴重錯誤：yfinance 模組無法載入。請確認 requirements.txt 已正確上傳至根目錄。")
