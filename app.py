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
                ticker_symbol = f"{t}.TW"
                stock = yf.Ticker(ticker_symbol)
                hist = stock.history(period="6mo")
                
                # 檢查是否取得有效資訊
                if hist.empty:
                    st.error(f"無法在 Yahoo Finance 找到代號 {ticker_symbol} 的數據，請確認代號是否正確。")
                elif len(hist) < 14:
                    st.error("該股票歷史數據不足（可能剛上市或交易稀疏），無法計算技術指標。")
                else:
                    hist = calculate_indicators(hist)
                    info = stock.info
                    
                    # 取得最新指標數值
                    rsi_val = hist['RSI'].iloc[-1]
                    macd_val = hist['MACD'].iloc[-1]
                    signal_val = hist['Signal'].iloc[-1]
                    
                    # 即時數據面板
                    curr = info.get('currentPrice', 'N/A')
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("即時股價", f"{curr}")
                    col2.metric("RSI (14日)", f"{rsi_val:.2f}")
                    col3.metric("MACD 差值", f"{macd_val:.2f}")
                    col4.metric("產業別", info.get('sector', 'N/A'))
                    
                    # AI 分析
                    prompt = f"""
                    請針對 {ticker_symbol} 進行全方位深度分析：
                    1. 【新聞動態分析】：市場觀點與近期重要新聞。
                    2. 【基本面與財務狀況】：PE、EPS、PB 等數據分析。
                    3. 【技術指標分析】：
                       - RSI 為 {rsi_val:.2f} (70以上超買, 30以下超賣)。
                       - MACD ({macd_val:.2f}) 與訊號線 ({signal_val:.2f}) 之關係。
                    4. 【黑天鵝警示】：分析潛在的結構性風險。
                    5. 【最終策略】：具體進出場建議。
                    """
                    response = client.chat.completions.create(
                        model="openai/gpt-4o-mini", 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    st.markdown("### 🎯 AI 綜合戰情報告")
                    st.write(response.choices[0].message.content)
                    
                    st.markdown("### 📊 股價與技術指標分析")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name="收盤價"))
                    st.plotly_chart(fig, width='stretch')

            except Exception as e:
                st.error(f"系統分析異常: {e}")

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
            st.success("總市值計算中...")
