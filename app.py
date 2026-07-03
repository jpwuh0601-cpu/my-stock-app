import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except:
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("目前沒有有效的數據，請稍候。")
        return

    # 顯示選單，將 Key 轉為清單
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇股票代號", tickers)
    
    # 確保選到的資料是字典結構
    ticker_data = data.get(selected_ticker)
    if not isinstance(ticker_data, dict):
        st.error("該股票資料結構錯誤，請等待下次自動更新。")
        return
    
    st.header(f"監控目標: {selected_ticker}")
    st.metric("即時股價", f"{float(ticker_data.get('price', 0)):,.2f}")
    
    st.subheader("🤖 AI 智能分析")
    st.info(str(ticker_data.get("ai_prediction", "暫無分析")))

if __name__ == "__main__":
    main()
