import streamlit as st
import json
import os
import time

st.set_page_config(page_title="AI 投資秘書儀表板", layout="wide")
st.title("📈 AI 投資秘書儀表板")

def load_data():
    """使用簡單且強固的方式載入數據"""
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"數據讀取錯誤: {e}")
            return None
    return None

# 讀取數據
data = load_data()

if data and isinstance(data, dict):
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇分析個股", tickers)
    
    ticker_data = data.get(selected_ticker, {})
    st.header(f"個股分析: {selected_ticker}")
    
    st.metric("目前價格", ticker_data.get('price', '資料載入中...'))
    
    st.subheader("🤖 AI 深度分析")
    st.write(ticker_data.get('ai_report', '分析生成中...'))
else:
    st.warning("正在初始化系統，請稍候幾秒鐘，若持續出現此訊息請檢查 market_data.json 是否已生成。")
    if st.button("手動刷新"):
        st.rerun()
