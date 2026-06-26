import streamlit as st
import yfinance as yf
import pandas as pd
from openai import OpenAI
import plotly.graph_objects as go

# 1. 頁面配置
st.set_page_config(page_title="股票分析助手", layout="wide")

# 2. 安全讀取 Secrets (金鑰存放在 Streamlit Cloud Settings)
try:
    # 這裡會自動從您在 Streamlit Cloud 設定的 Secrets 中讀取
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("系統偵測到 Secrets 設定異常，請至 Streamlit Cloud 設定 (Settings -> Secrets)。")
    st.stop()

st.title("📈 股票分析與即時監控助手")

# 3. 側邊欄參數
st.sidebar.header("設定參數")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
start_date = st.sidebar.date_input("開始日期", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("結束日期", pd.to_datetime("today"))

# 4. 強效資料抓取函數 (已移除 pandas_ta)
@st.cache_data(ttl=3600)
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end, timeout=10)
        return data
    except Exception as e:
        return None

# 5. AI 分析函數
def get_ai_summary(ticker_name):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"請分析這支股票的市場趨勢與風險: {ticker_name}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析發生錯誤: {e}"

# 6. 主程式邏輯
if st.sidebar.button("開始分析"):
    with st.spinner("正在連線抓取數據..."):
        df = get_stock_data(ticker, start_date, end_date)
        
        if df is not None and not df.empty:
            st.subheader(f"{ticker} 走勢分析")
            
            # 使用 Plotly 繪製蠟燭圖
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
            
            # 顯示原始數據摘要
            st.write("最新收盤數據:", df.tail())
            
            # AI 觀點
            st.subheader("AI 專家觀點")
            ai_text = get_ai_summary(ticker)
            st.write(ai_text)
        else:
            st.error("無法取得數據，請確認代號（如 2330.TW）或稍後再試。")

st.sidebar.markdown("---")
st.sidebar.success("系統狀態：線上")
