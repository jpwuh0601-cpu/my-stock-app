import streamlit as st
import json
import os

st.set_page_config(page_title="AI 投資秘書儀表板", layout="wide")

st.title("📈 AI 投資秘書儀表板")

def load_data():
    # 強制使用腳本所在的絕對路徑
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "market_data.json")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案存在但無法解析: {e}")
            return None
    else:
        st.error(f"系統找不到檔案，路徑應為: {file_path}")
        return None

data = load_data()

if data:
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇分析個股", tickers)
    
    ticker_data = data.get(selected_ticker, {})
    st.header(f"個股分析: {selected_ticker}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("目前價格", ticker_data.get('price', 'N/A'))
        
    st.subheader("🤖 AI 深度分析")
    st.markdown(ticker_data.get('ai_report', '分析生成中...'))
else:
    st.warning("數據讀取中或尚未產生，請稍候。")
