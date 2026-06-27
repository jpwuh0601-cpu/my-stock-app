import streamlit as st
import yfinance as yf
import pandas as pd
import time
from ai_engine import get_ai_analysis

# 設定網頁標題
st.set_page_config(page_title="股市 AI 決策系統", layout="wide")
st.title("📊 專業股市 AI 決策系統")

# 輸入區塊
ticker_input = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")

# 整理代號格式
ticker = ticker_input.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.button("查詢分析"):
    with st.spinner(f"正在為您連線至 Yahoo Finance 獲取 {ticker} 資料..."):
        try:
            # 使用 download 方法，這比 Ticker.history 更不容易被封鎖
            # 加入 auto_adjust=True 取得調整後價格
            df = yf.download(ticker, period="1mo", auto_adjust=True, progress=False)
            
            if df.empty:
                st.error(f"無法取得代號 {ticker} 的資料。")
                st.write("除錯建議：請確認代號是否為 Yahoo Finance 格式（台股請加 .TW），或稍候 5 分鐘再試。")
            else:
                # 取得最新收盤價與計算 MA20
                current_price = float(df['Close'].iloc[-1])
                ma20 = float(df['Close'].rolling(window=20).mean().iloc[-1])
                trend = "多頭" if current_price > ma20 else "空頭"
                
                # 顯示結果
                st.subheader(f"標的: {ticker} 數據概覽")
                col1, col2 = st.columns(2)
                col1.metric("最新收盤價", f"{round(current_price, 2)}")
                col2.metric("20日均線", f"{round(ma20, 2)}")
                st.write(f"### 趨勢狀態: {trend}")
                
                # 更新狀態給 AI 使用
                st.session_state['stock_data_summary'] = f"股票: {ticker}, 最新收盤價: {current_price}, 20日均線: {ma20}, 趨勢: {trend}"
                st.success("資料抓取成功！")
                
        except Exception as e:
            st.error(f"連線失敗，請稍後再試。系統錯誤代碼: {e}")

# AI 分析區塊
st.markdown("---")
st.markdown("### 🤖 AI 深度解讀")

if 'stock_data_summary' in st.session_state:
    if st.button("點擊產生 AI 分析建議"):
        with st.spinner("AI 正在深度解讀數據..."):
            try:
                analysis_result = get_ai_analysis(st.session_state['stock_data_summary'])
                st.write(analysis_result)
            except Exception as e:
                st.error("AI 分析服務暫時無法回應，請稍後再試。")
else:
    st.info("請先輸入股票代號並查詢，以進行 AI 分析。")
