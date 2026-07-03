import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    file_path = "market_data.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_history(ticker_symbol="2330.TW"):
    """即時抓取歷史股價"""
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="1mo")
    return hist

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    # 核心指標
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(data.get('price', 0)):,.2f}")
    
    st.divider()

    # 繪製歷史走勢圖
    st.subheader("📊 近一個月股價走勢")
    hist_data = get_history()
    if not hist_data.empty:
        fig = px.line(hist_data, y="Close", title="台積電 (2330.TW) 歷史股價")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("無法獲取歷史數據。")

    st.subheader("🏦 三大法人籌碼數據")
    raw = data.get("institutional_investors", [])
    if isinstance(raw, list) and len(raw) > 0:
        flattened_data = [{str(k): str(v) for k, v in item.items()} for item in raw]
        st.table(pd.DataFrame(flattened_data))
    else:
        st.info("目前無籌碼數據。")

    st.subheader("🤖 AI 智能分析")
    st.write(data.get("ai_prediction", "暫無分析數據。"))

if __name__ == "__main__":
    main()
