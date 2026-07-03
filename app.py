import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        selected = st.selectbox("監控標的", tickers)
        if st.button("確認選擇"):
            st.session_state.selected_ticker = selected

    info = data.get(st.session_state.get("selected_ticker", tickers[0]), {})
    
    st.subheader(f"{st.session_state.get('selected_ticker', tickers[0])} 即時財報")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
    col2.metric("EPS", f"{info.get('eps', 0):,.2f}")
    col3.metric("本益比", f"{info.get('pe', 0):,.2f}")
    
    st.info(f"AI 分析快評: {info.get('ai_prediction', '分析中...')}")
    st.write(f"系統最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
