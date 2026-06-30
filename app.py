import streamlit as st
import json
import os
import yfinance as yf
import pandas as pd
import time

# 設定頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 使用快取來避免觸發 Rate Limit
@st.cache_data(ttl=600)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1mo") # 擴大至一個月以利技術指標分析
        return hist
    except Exception as e:
        return None

# 讀取分析數據
def load_market_data():
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

# 側邊欄查詢
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")
search_button = st.sidebar.button("開始搜尋")

if search_button and ticker_input:
    ticker_symbol = f"{ticker_input}.TW"
    
    with st.spinner("正在進行 AI 深度分析..."):
        hist = get_stock_data(ticker_symbol)
        data = load_market_data()
        
        if hist is None or hist.empty:
            st.error(f"無法取得 {ticker_symbol} 的資料。")
        else:
            current_price = hist['Close'].iloc[-1]
            st.subheader(f"代碼: {ticker_input} 最新價格: {current_price:.2f}")
            
            # --- 儀表板顯示 ---
            tab1, tab2, tab3 = st.tabs(["AI 智能分析與策略", "技術指標與警示", "新聞與基本面"])
            
            with tab1:
                st.write("### 🤖 GPT AI 綜合評估")
                st.info(data.get("ai_prediction", "暫無分析數據"))
                st.success(f"選股建議: {data.get('ai_stock_selection', '持平')}")
            
            with tab2:
                col1, col2, col3 = st.columns(3)
                ti = data.get("technical_indicators", {})
                col1.metric("RSI (強弱)", f"{ti.get('RSI', 0):.2f}")
                col2.write(f"MACD: {ti.get('MACD', 'N/A')}")
                col3.error(f"黑天鵝警示: {'⚠️ 已觸發' if data.get('black_swan_alert', {}).get('is_triggered') else '✅ 安全'}")
            
            with tab3:
                st.write("### 🗞️ 市場新聞")
                for news in data.get("news", ["無最新新聞"]):
                    st.write(f"- {news}")
                col1, col2 = st.columns(2)
                col1.metric("預估 EPS", data.get("est_eps", "N/A"))
                col2.metric("預估股利", data.get("est_dividend", "N/A"))
            
elif search_button and not ticker_input:
    st.sidebar.warning("請先輸入代碼！")
else:
    st.write("請在側邊欄輸入代碼並點選「開始搜尋」。")

# 頁尾狀態
st.sidebar.markdown("---")
st.sidebar.caption("系統狀態: 🟢 LINE 通知已連線")
if os.path.exists("market_data.json"):
    st.sidebar.caption(f"數據最後更新: {pd.to_datetime(os.path.getmtime('market_data.json'), unit='s')}")
