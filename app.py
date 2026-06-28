import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定頁面風格
st.set_page_config(page_title="AI 專業投資儀表板", layout="wide", page_icon="📈")

st.title("📈 AI 專業投資決策中樞 (專業版)")

# 安全讀取環境變數
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
)

# 頁面內容
menu = st.sidebar.radio("導航目錄", ["🤖 個股深度分析", "💼 部位管理"])

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

if menu == "🤖 個股深度分析":
    st.subheader("個股即時數據健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        with st.spinner("正在抓取數據與運算指標..."):
            try:
                ticker_symbol = f"{t}.TW"
                stock = yf.Ticker(ticker_symbol)
                hist = stock.history(period="6mo") # 延長數據以利指標運算
                info = stock.info
                
                # 即時指標面板
                curr = info.get('currentPrice', 0)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("即時股價", f"{curr:.2f}")
                col2.metric("本益比", info.get('trailingPE', 'N/A'))
                col3.metric("每股淨值", info.get('priceToBook', 'N/A'))
                col4.metric("RSI (14日)", f"{calculate_rsi(hist['Close']).iloc[-1]:.2f}")
                
                # AI 分析
                funda_data = {"名稱": info.get('longName'), "產業": info.get('sector'), "EPS": info.get('trailingEps')}
                prompt = f"分析 {ticker_symbol}，重點關注基本面與近期技術面建議。"
                response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                st.markdown("### 🎯 AI 深度健檢")
                st.write(response.choices[0].message.content)
                
                # 技術指標圖表
                st.markdown("### 📊 股價與 RSI 指標")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name="收盤價"))
                st.plotly_chart(fig, width='stretch')

            except Exception as e:
                st.error(f"資料抓取失敗: {e}")

elif menu == "💼 部位管理":
    st.subheader("我的持股看板")
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = pd.DataFrame(columns=["代號", "成本", "股數"])
    
    with st.form("add_stock"):
        c1, c2, c3 = st.columns(3)
        symbol = c1.text_input("代號")
        cost = c2.number_input("成本價", value=0.0)
        shares = c3.number_input("股數", value=0)
        if st.form_submit_button("新增持股"):
            new_row = pd.DataFrame({"代號": [symbol], "成本": [cost], "股數": [shares]})
            st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_row], ignore_index=True)
    
    if not st.session_state.portfolio.empty:
        st.table(st.session_state.portfolio)
        if st.button("計算總損益"):
            st.success("功能已就緒，請連接即時行情計算盈虧。")
