import streamlit as st
import json
import os
import plotly.express as px
import yfinance as yf

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_data()
ticker_input = st.selectbox("請選擇監控標的", list(data.keys()) if data else ["2330.TW"])

if ticker_input in data:
    m = data[ticker_input]
    
    # 指標顯示
    c1, c2, c3 = st.columns(3)
    c1.metric("即時股價", f"{m['price']:.2f}")
    c2.metric("本益比", f"{m['pe']:.2f}")
    c3.metric("EPS", f"{m['eps']:.2f}")
    
    # AI 分析區塊
    st.subheader("🤖 AI 顧問分析")
    st.info(m["ai_prediction"])
    
    # 風險區塊
    st.warning(f"當前風險狀態: {m['black_swan']}")
    
    # 歷史走勢圖
    st.subheader("📈 股價走勢")
    hist = yf.Ticker(ticker_input).history(period="1mo")
    fig = px.line(hist, y="Close", title=f"{ticker_input} 近期走勢")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("數據載入中或檔案遺失，請檢查 GitHub Actions 執行狀態。")
