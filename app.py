import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from openai import OpenAI
import plotly.graph_objects as go

# 1. 頁面配置
st.set_page_config(page_title="股票分析助手", layout="wide")

# 2. 安全讀取 Secrets (務必確認 Streamlit Cloud 已填入 LINE_CHANNEL_ACCESS_TOKEN)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Secrets 設定異常，請至 Streamlit Cloud 設定 (Settings -> Secrets)。")
    st.stop()

st.title("📈 股票分析與即時監控助手")

# 3. 側邊欄參數
st.sidebar.header("設定參數")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
start_date = st.sidebar.date_input("開始日期", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("結束日期", pd.to_datetime("today"))

# 4. 功能函數
@st.cache_data(ttl=3600)
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, timeout=10)
        return data
    except Exception:
        return None

def get_ai_summary(ticker_name):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"請分析這支股票的市場趨勢與風險: {ticker_name}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"分析失敗: {e}"

def send_line_notify(message):
    try:
        token = st.secrets["LINE_CHANNEL_ACCESS_TOKEN"]
        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"message": message}
        requests.post(url, headers=headers, data=payload)
    except Exception:
        pass # 若 LINE 設定未完成則靜默處理

# 5. 主邏輯
if st.sidebar.button("分析並傳送到 LINE"):
    with st.spinner("正在分析並傳送..."):
        df = get_stock_data(ticker, start_date, end_date)
        
        if df is not None and not df.empty:
            st.subheader(f"{ticker} 走勢分析")
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
            
            ai_text = get_ai_summary(ticker)
            st.write("AI 分析結果:", ai_text)
            
            # 觸發 LINE 通知
            send_line_notify(f"\n【股票分析報告】\n代號: {ticker}\n分析結果: {ai_text}")
            st.success("分析報告已成功發送到您的 LINE！")
        else:
            st.error("無法取得數據，請輸入正確代號 (例如 2330.TW)。")

st.sidebar.markdown("---")
st.sidebar.success("系統狀態：線上")
