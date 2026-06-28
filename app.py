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
    
    # 提供用戶常見代號檢查提示
    with st.expander("⚠️ 若分析失敗，請檢查："):
        st.write("1. 確保代號為台灣上市櫃股票 (如 2330, 2454)。")
        st.write("2. Yahoo Finance 若查無數據，請確認該代號是否正確或已下市。")
        st.write("3. 嘗試手動加上 .TW (上市) 或 .TWO (上櫃) 後綴。")

    if st.button("啟動專業分析"):
        with st.spinner("正在進行多維度分析..."):
            try:
                # 改進的代號處理邏輯：優先嘗試用戶輸入，若失敗則嘗試補上 TW
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
                
                # 深度數據檢查
                if hist is None or hist.empty:
                    st.error(f"無法在 Yahoo Finance 找到代號 **{t}** 的相關數據 (嘗試過: {', '.join(tickers_to_try)})。請確認代號正確性。")
                elif len(hist) < 14:
                    st.error("該股票歷史數據不足，無法進行 RSI/MACD 等指標計算。")
                else:
                    hist = calculate_indicators(hist)
                    info = stock.info
                    
                    # 取得最新指標數值
                    rsi_val = hist['RSI'].iloc[-1]
                    macd_val = hist['MACD'].iloc[-1]
                    
                    # 即時數據面板
                    curr = info.get('currentPrice', 'N/A')
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("即時股價", f"{curr}")
                    col2.metric("RSI (14日)", f"{rsi_val:.2f}")
                    col3.metric("MACD 差值", f"{macd_val:.2f}")
                    col4.metric("產業別", info.get('sector', 'N/A'))
                    
                    # AI 分析指令
                    prompt = f"""
                    請針對 {ticker_formatted} 進行全方位深度分析：
                    1. 【新聞動態】：市場觀點與近期重要新聞。
                    2. 【技術指標判讀】：RSI ({rsi_val:.2f}) 與 MACD ({macd_val:.2f}) 之趨勢分析。
                    3. 【風險評估】：針對該股進行黑天鵝風險評估。
                    4. 【策略建議】：給出具體進出場判斷。
                    """
                    response = client.chat.completions.create(
                        model="openai/gpt-4o-mini", 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    st.markdown("### 🎯 AI 綜合戰情報告")
                    st.write(response.choices[0].message.content)
                    
                    st.markdown("### 📊 股價走勢")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name="收盤價", line=dict(color='royalblue')))
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"分析過程發生非預期錯誤: {e}")

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
