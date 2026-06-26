import streamlit as st
import yfinance as yf
import pandas as pd
from openai import OpenAI
import plotly.graph_objects as go

# 1. 頁面配置
st.set_page_config(page_title="股票分析助手", layout="wide")

# 2. 安全讀取 Secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    line_token = st.secrets["LINE_CHANNEL_ACCESS_TOKEN"]
except Exception as e:
    st.error("系統偵測到 Secrets 設定異常，請檢查 Streamlit Cloud 的 Settings -> Secrets。")
    st.stop()

st.title("📈 股票分析與即時監控助手")

# 3. 側邊欄設定
st.sidebar.header("設定參數")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
start_date = st.sidebar.date_input("開始日期", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("結束日期", pd.to_datetime("today"))

# 4. 資料抓取函數
@st.cache_data
def get_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        return data
    except Exception as e:
        return None

# 5. AI 分析函數
def get_ai_summary(ticker_name):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"請幫我用專業角度分析這支股票的走勢: {ticker_name}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析發生錯誤: {e}"

# 6. 主程式邏輯
if st.sidebar.button("開始分析"):
    with st.spinner("正在抓取數據與運算中..."):
        df = get_stock_data(ticker, start_date, end_date)
        
        if df is not None and not df.empty:
            st.subheader(f"{ticker} 歷史走勢")
            
            # 使用 Plotly 繪製蠟燭圖
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'])])
            st.plotly_chart(fig, use_container_width=True)
            
            # 顯示原始數據摘要
            st.write("最新股價數據:", df.tail())
            
            # AI 總結
            st.subheader("AI 專家觀點")
            ai_text = get_ai_summary(ticker)
            st.write(ai_text)
        else:
            st.error("無法取得數據，請確認股票代號格式是否正確（例如台股需加上 .TW）。")

st.sidebar.markdown("---")
st.sidebar.success("系統狀態：正常運作中")
