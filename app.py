import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import os
from datetime import datetime

st.set_page_config(page_title="金融儀表板", layout="wide")

# 顯示最後更新時間
if os.path.exists("analysis_result.txt"):
    mtime = os.path.getmtime("analysis_result.txt")
    st.sidebar.info(f"上次更新: {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")

st.title("📊 專業金融分析終端")

ticker = st.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")

if st.button("執行分析"):
    # 1. 繪製走勢圖 (Plotly)
    hist = yf.Ticker(ticker).history(period="1mo")
    fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
    fig.update_layout(title=f"{ticker} 近一個月走勢", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. 顯示 AI 分析 (依據您的檔案架構)
    if os.path.exists("analysis_result.txt"):
        with open("analysis_result.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        tab1, tab2 = st.tabs(["AI 深度報告", "籌碼表格"])
        with tab1:
            st.markdown(content)
        with tab2:
            st.write("請見原始報告中的表格區域")
