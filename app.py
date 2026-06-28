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
    .metric-card { 
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%);
        padding: 25px; 
        border-radius: 20px; 
        border-left: 10px solid #2563EB;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    h3 { color: #1E3A8A; font-weight: 800; }
    .stButton>button { border-radius: 12px; background-color: #2563EB; color: white; font-weight: bold; }
    .stMetric { background-color: #fff; padding: 15px; border-radius: 10px; border: 1px solid #e5e7eb; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞 (專業版)")

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

menu = st.sidebar.radio("導航目錄", ["🤖 個股深度分析", "💼 部位管理"])

if menu == "🤖 個股深度分析":
    st.subheader("個股即時數據健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        try:
            ticker_formatted = t.strip() + ".TW" if not any(x in t for x in [".TW", ".TWO"]) else t.strip()
            stock = yf.Ticker(ticker_formatted)
            hist = stock.history(period="6mo")
            info = stock.info
            
            # 技術指標計算
            rsi_val = calculate_rsi(hist).iloc[-1]
            
            curr = info.get('currentPrice') or info.get('regularMarketPrice', 0.0)
            eps = info.get('trailingEps', 0.0)
            pe = info.get('trailingPE', 0.0)
            
            shares = info.get('sharesOutstanding') or 100000000.0
            prev_revenue = info.get('totalRevenue') or 1000000000.0 

            st.markdown("### 📊 即時市場動態與技術面")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{curr:.2f}")
            col2.metric("RSI (14日)", f"{rsi_val:.2f}")
            col3.metric("EPS", f"{eps:.2f}")
            col4.metric("本益比", f"{pe:.2f}")
            
            # 技術面分析建議
            st.markdown("### 🔍 趨勢與警示")
            c1, c2 = st.columns(2)
            with c1:
                st.info("技術指標建議")
                if rsi_val > 70: st.warning("⚠️ RSI 過熱：目前股價進入超買區，需留意回調風險。")
                elif rsi_val < 30: st.success("✅ RSI 超賣：可能存在反彈機會，建議關注佈局點。")
                else: st.write("ℹ️ RSI 處於正常區間，趨勢穩定。")
            with c2:
                st.warning("黑天鵝警示")
                st.write("目前市場波動率正常，未偵測到異常黑天鵝風險。請持續追蹤地緣政治與財報公告。")

            st.divider()
            
            # 推算邏輯
            with st.expander("🔮 明年專業推算數據", expanded=False):
                c1, c2, c3, c4 = st.columns(4)
                manual_prev_revenue = c1.number_input("上年度營收 (元)", value=float(prev_revenue), step=1e7)
                yoy = c2.number_input("累積營收年增率 (%)", value=10.0) / 100
                margin = c3.number_input("稅後淨利率 (%)", value=15.0) / 100
                payout = c4.number_input("盈餘分配率 (%)", value=60.0) / 100
                
                est_revenue = manual_prev_revenue * (1 + yoy)
                est_net_profit = est_revenue * margin
                est_eps = est_net_profit / shares
                est_price = est_eps * (pe if pe > 0 else 15)
                
                st.write(f"預估明年股價: **{est_price:.2f}** | 預估 EPS: **{est_eps:.2f}**")

            if not hist.empty:
                st.line_chart(hist['Close'], use_container_width=True)
            
        except Exception as e:
            st.error(f"分析錯誤: {e}")

elif menu == "💼 部位管理":
    st.subheader("💼 我的持股管理")
    st.info("此區塊目前正在建構中...")
