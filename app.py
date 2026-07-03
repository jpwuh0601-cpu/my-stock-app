import streamlit as st
import json
import pandas as pd
import plotly.express as px

# ... (前面 load_data 函式保持不變)

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    if not data: return

    # 側邊欄建立表單
    with st.sidebar.form(key='ticker_form'):
        selected_ticker = st.selectbox("請選擇股票代號", list(data.keys()))
        submit_button = st.form_submit_button(label='確定分析')

    # 只有按下按鈕時，才執行後續邏輯
    if submit_button:
        ticker_data = data.get(selected_ticker)
        st.header(f"監控目標: {selected_ticker}")
        st.metric("即時股價", f"{float(ticker_data.get('price', 0)):,.2f}")
        st.info(str(ticker_data.get("ai_prediction", "暫無分析")))
    else:
        st.write("請從左側選擇股票並點擊「確定分析」按鈕。")

if __name__ == "__main__":
    main()
