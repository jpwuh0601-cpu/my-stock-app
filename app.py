import streamlit as st
import yfinance as yf
import pandas as pd
import time
from ai_engine import get_ai_analysis

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 輸入區塊
ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")

if st.button("查詢分析"):
    with st.spinner("正在從 Yahoo Finance 抓取資料..."):
        try:
            # 加入緩衝機制，避免頻繁請求導致 YFRateLimitError
            time.sleep(1)
            
            # 抓取股票資料
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1mo")
            
            # 檢查是否成功取得資料
            if info is None or hist.empty:
                st.error("無法取得該代號的資料，請確認輸入是否正確。")
            else:
                # 顯示關鍵指標
                st.subheader(f"標的: {ticker} 關鍵指標")
                col1, col2, col3 = st.columns(3)
                col1.metric("即時報價", f"{info.get('currentPrice', 'N/A')}")
                col2.metric("漲跌幅", f"{round(info.get('regularMarketChangePercent', 0), 2)}%")
                col3.metric("EPS", f"{info.get('trailingEps', 'N/A')}")
                
                col4, col5, col6 = st.columns(3)
                col4.metric("本益比", f"{round(info.get('trailingPE', 0), 2)}")
                col5.metric("每股淨值", f"{round(info.get('bookValue', 0), 2)}")
                col6.metric("發行股數", f"{info.get('sharesOutstanding', 'N/A'):,}")
                
                # 簡單技術分析
                ma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                current_price = info.get('currentPrice', 0)
                trend = "多頭" if current_price > ma20 else "空頭"
                st.write(f"### 趨勢狀態: {trend} (20日均線: {round(ma20, 2)})")
                
                # 將數據轉為字串給 AI 使用
                stock_data_summary = f"股票: {ticker}, 目前價格: {current_price}, 趨勢: {trend}, EPS: {info.get('trailingEps')}"
                st.session_state['stock_data_summary'] = stock_data_summary
            
        except Exception as e:
            st.error(f"抓取資料發生錯誤 (請稍候再試): {e}")

# AI 分析區塊
st.markdown("---")
st.markdown("### 🤖 AI 深度解讀")

if 'stock_data_summary' in st.session_state:
    if st.button("點擊產生 AI 分析建議"):
        with st.spinner("AI 正在分析中..."):
            # 呼叫正確的函式名稱
            analysis_result = get_ai_analysis(st.session_state['stock_data_summary'])
            st.write(analysis_result)
else:
    st.info("請先查詢一支股票以進行 AI 分析。")
