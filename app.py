import streamlit as st
import json
import os
import plotly.express as px
import yfinance as yf

st.set_page_config(layout="wide", page_title="專業金融監控終端")
st.title("📊 專業金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

# 確保下拉選單有內容，若為空則顯示提示
ticker_options = list(data.keys()) if data else ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"]
ticker_input = st.selectbox("請選擇監控標的", ticker_options)

if ticker_input in data:
    m = data[ticker_input]
    
    # 財務數據顯示
    c1, c2, c3 = st.columns(3)
    c1.metric("即時股價", f"{m.get('price', 0):.2f}")
    c2.metric("本益比", f"{m.get('pe', 0):.2f}")
    c3.metric("EPS", f"{m.get('eps', 0):.2f}")
    
    # AI 分析區塊
    st.subheader("🤖 AI 顧問分析")
    st.info(m.get("ai_prediction", "AI 分析引擎待命中..."))
    
    # 風險狀態
    st.warning(f"當前風險狀態: {m.get('black_swan', '未知')}")
    
    # 股價走勢圖 (強連結選定標的)
    st.subheader(f"📈 {ticker_input} 歷史走勢")
    hist = yf.Ticker(ticker_input).history(period="1mo")
    if not hist.empty:
        fig = px.line(hist, y="Close", title=f"{ticker_input} 近期走勢")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("目前無法獲取歷史走勢圖表。")
else:
    st.error(f"目前 {ticker_input} 的詳細籌碼與分析數據尚未同步。請檢查 GitHub Actions 執行情況。")
