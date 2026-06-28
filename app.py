import streamlit as st
import yfinance as yf
import pandas as pd
import requests_cache

# 設定頁面配置
st.set_page_config(page_title="股市決策系統", layout="wide")

# 設定偽裝瀏覽器請求，解決 Yahoo Finance 偶發性連線問題
session = requests_cache.CachedSession('yfinance.cache', expire_after=3600)
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# 側邊欄導航
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 數據載入函數
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.TW", session=session)
        hist = stock.history(period="1mo")
        return hist, stock.info
    except Exception as e:
        return None, str(e)

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 使用 Form 結構：確保「啟動分析」按鈕被按下才發送請求
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner('正在從財經資料庫同步資訊...'):
            df, info = get_stock_data(ticker)
            
            if df is not None and not df.empty:
                # 顯示市場動態卡片
                st.subheader("📊 即時市場動態")
                cols = st.columns(4)
                cols[0].metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
                cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                cols[3].metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                
                # 顯示趨勢圖
                st.subheader("📈 股價走勢")
                st.line_chart(df['Close'])
            else:
                st.error("無法連線至財經資料庫，請稍後再試。")

elif menu == "部位管理":
    st.title("💼 部位管理系統")
    st.write("您可以在此檢視您的投資組合與持倉績效。")
    
    # 顯示部位列表
    portfolio_data = pd.DataFrame({
        "股票代號": ["2330", "2881"],
        "持倉成本": [600.0, 50.0],
        "目前市價": [1050.0, 75.0]
    })
    st.table(portfolio_data)
    st.success("部位數據已同步。")
