import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import yfinance as yf
from datetime import datetime
from openai import OpenAI

# 設定頁面風格
st.set_page_config(layout="wide", page_title="AI 專業投資儀表板", page_icon="📈")

# 自定義 CSS
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: bold; }
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞 (專業版)")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
)

menu = st.sidebar.radio("導航目錄", ["🤖 個股深度分析", "💼 部位管理"])

def calculate_indicators(data):
    if len(data) < 14: return None
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

if menu == "🤖 個股深度分析":
    st.subheader("個股即時數據健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        try:
            ticker_formatted = t.strip() + ".TW" if not any(x in t for x in [".TW", ".TWO"]) else t.strip()
            stock = yf.Ticker(ticker_formatted)
            hist = stock.history(period="6mo")
            info = stock.info
            
            curr = info.get('currentPrice', 0.0)
            eps = info.get('trailingEps', 0.0)
            pe = info.get('trailingPE', 0.0)
            bv = info.get('bookValue', 0.0)
            shares = info.get('sharesOutstanding', 1)
            # 獲取上年度營收 (若無則預估)
            prev_revenue = info.get('totalRevenue', 0)

            st.markdown("### 📊 即時市場動態")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{curr:.2f}")
            col2.metric("EPS", f"{eps:.2f}")
            col3.metric("本益比", f"{pe:.2f}")
            col4.metric("每股淨值", f"{bv:.2f}")
            
            st.divider()

            if 'show_forecast' not in st.session_state: st.session_state.show_forecast = False
            if st.button("查看預估明年股價"): st.session_state.show_forecast = True
            
            if st.session_state.show_forecast:
                st.markdown("### 🔮 明年專業推算數據 (八步驟邏輯)")
                with st.expander("設定推算參數", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    yoy = c1.number_input("累積營收年增率 (%)", value=10.0) / 100
                    margin = c2.number_input("稅後淨利率 (%)", value=15.0) / 100
                    payout = c3.number_input("盈餘分配率 (%)", value=60.0) / 100
                    target_pe = c4.number_input("預期本益比", value=float(pe) if pe else 15.0)
                
                # 推算邏輯實作
                est_revenue = prev_revenue * (1 + yoy)  # 今預估營收
                est_net_profit = est_revenue * margin   # 預估稅後淨利
                est_eps = est_net_profit / shares if shares > 0 else 0 # 預估 EPS
                est_dividend = est_eps * payout         # 預估現金股利
                est_price = est_eps * target_pe         # 預估明年股價

                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年股價", f"{est_price:.2f}")
                p2.metric("預估 EPS", f"{est_eps:.2f}")
                p3.metric("預估現金股利", f"{est_dividend:.2f}")
                p4.metric("預估今年營收", f"{est_revenue/1e9:.2f} B")

            st.markdown("### 📈 股價走勢")
            st.line_chart(hist['Close'])

        except Exception as e:
            st.error(f"分析過程錯誤: {e}")

elif menu == "💼 部位管理":
    st.subheader("我的持股看板")
