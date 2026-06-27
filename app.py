import streamlit as st
import yfinance as yf
import pandas as pd
import time
from ai_engine import get_ai_analysis

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 輸入區塊
ticker = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")

# 自動處理台股代號補全功能
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.button("查詢分析"):
    with st.spinner(f"正在安全抓取 {ticker} 的資料..."):
        try:
            # 加入緩衝機制
            time.sleep(2)
            
            # 使用 yf.download 方式
            df = yf.download(ticker, period="1mo", progress=False)
            
            # 檢查是否成功取得資料
            if df.empty:
                st.error(f"無法取得代號 {ticker} 的資料，請確認輸入代號是否正確。")
            else:
                # 取得最新收盤價
                current_price = df['Close'].iloc[-1]
                if isinstance(current_price, pd.Series):
                    current_price = current_price.iloc[0]
                
                # 簡單技術分析
                ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
                if isinstance(ma20, pd.Series):
                    ma20 = ma20.iloc[0]
                    
                trend = "多頭" if current_price > ma20 else "空頭"
                
                # 顯示關鍵數據
                st.subheader(f"標的: {ticker} 數據概覽")
                col1, col2 = st.columns(2)
                col1.metric("最新收盤價", f"{round(float(current_price), 2)}")
                col2.metric("20日均線", f"{round(float(ma20), 2)}")
                
                st.write(f"### 趨勢狀態: {trend}")
                
                # 將數據轉為字串給 AI 使用
                stock_data_summary = f"股票: {ticker}, 最新收盤價: {current_price}, 20日均線: {ma20}, 趨勢: {trend}"
                st.session_state['stock_data_summary'] = stock_data_summary
            
        except Exception as e:
            st.error(f"抓取資料發生錯誤，建議檢查代號或稍候再試: {e}")

# AI 分析區塊
st.markdown("---")
st.markdown("### 🤖 AI 深度解讀")

if 'stock_data_summary' in st.session_state:
    if st.button("點擊產生 AI 分析建議"):
        with st.spinner("AI 正在分析中..."):
            analysis_result = get_ai_analysis(st.session_state['stock_data_summary'])
            st.write(analysis_result)
else:
    st.info("請先查詢一支股票以進行 AI 分析。")
