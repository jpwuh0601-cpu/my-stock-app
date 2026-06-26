import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import openai
from linebot import LineBotApi
import plotly.graph_objects as go
import os

# 使用 try-except 區塊來處理可能缺失的 Secrets，這比直接存取更安全
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    LINE_CHANNEL_ACCESS_TOKEN = st.secrets["LINE_CHANNEL_ACCESS_TOKEN"]
    # 如果有 LINE_CHANNEL_SECRET 也建議一起加入
except Exception as e:
    st.error(f"Secrets 設定錯誤，請確保在 Streamlit Cloud Settings 中有正確填入: {e}")
    st.stop()

st.set_page_config(page_title="股票分析助手", layout="wide")
st.title("📈 股票分析與即時監控助手")

st.sidebar.header("設定參數")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
start_date = st.sidebar.date_input("開始日期", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("結束日期", pd.to_datetime("today"))

@st.cache_data
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        return data
    except Exception as e:
        return None

if st.sidebar.button("分析股票"):
    with st.spinner("正在抓取數據與運算..."):
        df = get_stock_data(ticker, start_date, end_date)
        
        if df is not None and not df.empty:
            st.write(f"顯示 {ticker} 的歷史走勢")
            
            # 使用 Plotly 繪製股價圖
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
            
            # 簡單計算技術指標 (pandas-ta)
            df.ta.rsi(append=True)
            st.write("技術指標數據 (RSI):", df.tail())
        else:
            st.error("無法取得數據，請檢查股票代號是否正確。")

def get_ai_summary(ticker_data):
    # 此處整合 OpenAI 的邏輯
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"分析這支股票: {ticker}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析發生錯誤: {e}"
