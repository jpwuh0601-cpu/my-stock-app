import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def render_history_chart(history_data):
    if not history_data:
        st.write("暫無歷史數據可繪製")
        return
    df = pd.DataFrame(history_data)
    fig = px.line(df, x="date", y="close", title="近一個月股價走勢")
    fig.update_traces(line_color='#00CC96')
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0] if tickers else ""

    with st.sidebar:
        selected = st.selectbox("請選擇監控標的", tickers, index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0)
        if st.button("確認選擇"):
            st.session_state.selected_ticker = selected
            st.rerun()

    info = data.get(st.session_state.selected_ticker, {})
    st.header(f"監控標的: {st.session_state.selected_ticker}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
    
    render_history_chart(info.get("history", []))
    
    st.info(f"AI 分析: {info.get('ai_prediction', '分析中...')}")
    st.caption(f"最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
