import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定頁面風格
st.set_page_config(page_title="AI 專業投資儀表板", layout="wide", page_icon="📈")

# 自定義 CSS 讓方塊更有感
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞 (專業版)")

# 安全讀取環境變數
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
)

# 頁面內容
menu = st.sidebar.radio("導航目錄", ["🤖 個股深度分析", "💼 部位管理"])

def calculate_indicators(data):
    if len(data) < 14:
        return None
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data

if menu == "🤖 個股深度分析":
    st.subheader("個股即時數據健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        with st.spinner("正在進行多維度分析..."):
            try:
                ticker_input = t.strip()
                tickers_to_try = [ticker_input]
                if not ticker_input.endswith((".TW", ".TWO")):
                    tickers_to_try.append(f"{ticker_input}.TW")
                    tickers_to_try.append(f"{ticker_input}.TWO")
                
                hist = None
                stock = None
                ticker_formatted = ""

                for candidate in tickers_to_try:
                    stock = yf.Ticker(candidate)
                    hist = stock.history(period="6mo")
                    if not hist.empty:
                        ticker_formatted = candidate
                        break
                
                if hist is None or hist.empty:
                    st.error(f"無法找到代號 **{t}** 的數據。")
                else:
                    hist = calculate_indicators(hist)
                    info = stock.info
                    
                    # 抓取數據
                    curr = info.get('currentPrice', 0.0)
                    prev_close = info.get('previousClose', curr)
                    
                    # 計算漲跌金額與幅度
                    delta_val = curr - prev_close if curr and prev_close else 0
                    change_pct = (delta_val / prev_close * 100) if prev_close and prev_close != 0 else 0
                    
                    eps = info.get('trailingEps', 'N/A')
                    pe = info.get('trailingPE', 'N/A')
                    bv = info.get('bookValue', 'N/A')
                    shares = info.get('sharesOutstanding', 'N/A')

                    # 顯示即時股價數據面板 (彩色塊狀)
                    st.markdown("### 📊 即時市場動態")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("即時股價", f"{curr}", f"{delta_val:+.2f} ({change_pct:+.2f}%)")
                    col2.metric("EPS", f"{eps}")
                    col3.metric("本益比", f"{pe}")
                    col4.metric("每股淨值", f"{bv}")
                    col5.metric("發行股數", f"{shares:,}" if isinstance(shares, (int, float)) else shares)
                    
                    st.divider()

                    # 預估明年股價功能
                    if 'show_forecast' not in st.session_state:
                        st.session_state.show_forecast = False
                    
                    if st.button("查看預估明年股價"):
                        st.session_state.show_forecast = True
                    
                    if st.session_state.show_forecast:
                        st.markdown("### 🔮 明年預估數據")
                        p1, p2, p3, p4 = st.columns(4)
                        
                        est_eps = float(eps) * 1.1 if isinstance(eps, (int, float)) else "N/A"
                        est_price = float(curr) * 1.1 if isinstance(curr, (int, float)) else "N/A"
                        
                        # 使用字串格式化，確保即使數值為 N/A 也能顯示
                        p1.metric("預估股價", f"{est_price:.2f}" if isinstance(est_price, float) else "N/A")
                        p2.metric("預估 EPS", f"{est_eps:.2f}" if isinstance(est_eps, float) else "N/A")
                        p3.metric("本益比", f"{pe}")
                        p4.metric("每股淨值", f"{bv}")

                    # AI 分析
                    prompt = f"分析 {ticker_formatted}，當前股價: {curr}, EPS: {eps}, 本益比: {pe}, 淨值: {bv}"
                    response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                    st.markdown("### 🎯 AI 綜合戰情報告")
                    st.write(response.choices[0].message.content)
                    
                    st.markdown("### 📈 股價走勢圖")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name="收盤價", line=dict(color='#FF4B4B', width=2)))
                    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, width='stretch')

            except Exception as e:
                st.error(f"分析過程發生錯誤: {e}")

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
