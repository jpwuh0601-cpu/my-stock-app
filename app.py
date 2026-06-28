import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import yfinance as yf
from datetime import datetime

# 設定頁面風格
st.set_page_config(layout="wide", page_title="AI 專業投資儀表板", page_icon="📈")

# 自定義 CSS - 優化配色與鮮豔度
st.markdown("""
    <style>
    .metric-card { 
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px; 
        border-radius: 15px; 
        border-left: 8px solid #FF4B4B;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    h3 { color: #1E3A8A; }
    .stButton>button { border-radius: 10px; background-color: #1E3A8A; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞 (專業版)")

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
            
            # 安全數據獲取，避免拋出異常
            curr = info.get('currentPrice') or info.get('regularMarketPrice', 0.0)
            eps = info.get('trailingEps', 0.0)
            pe = info.get('trailingPE', 0.0)
            bv = info.get('bookValue', 0.0)
            shares = info.get('sharesOutstanding') or 100000000.0 # 預設值避免計算崩潰
            prev_revenue = info.get('totalRevenue') or 0.0

            st.markdown("### 📊 即時市場動態")
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("即時股價", f"{curr:.2f}")
            with col2: st.metric("EPS", f"{eps:.2f}")
            with col3: st.metric("本益比", f"{pe:.2f}")
            with col4: st.metric("每股淨值", f"{bv:.2f}")
            
            st.divider()

            if 'show_forecast' not in st.session_state: st.session_state.show_forecast = False
            if st.button("查看預估明年股價"): st.session_state.show_forecast = True
            
            if st.session_state.show_forecast:
                st.markdown("### 🔮 明年專業推算數據 (八步驟邏輯)")
                with st.expander("📝 調整推算參數 (若自動抓取為 0，請手動修正)", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    manual_prev_revenue = c1.number_input("上年度營收 (元)", value=float(prev_revenue), step=1e7)
                    yoy = c2.number_input("累積營收年增率 (%)", value=10.0) / 100
                    margin = c3.number_input("稅後淨利率 (%)", value=15.0) / 100
                    payout = c4.number_input("盈餘分配率 (%)", value=60.0) / 100
                    
                    c5, c6 = st.columns(2)
                    target_pe = c5.number_input("預期本益比 (P/E)", value=float(pe) if pe and pe > 0 else 15.0)
                    manual_shares = c6.number_input("發行股數", value=float(shares), step=1e6)
                
                # 推算邏輯
                est_revenue = manual_prev_revenue * (1 + yoy)
                est_net_profit = est_revenue * margin
                est_eps = est_net_profit / manual_shares if manual_shares > 0 else 0
                est_dividend = est_eps * payout
                est_price = est_eps * target_pe

                st.markdown("---")
                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年股價", f"{est_price:.2f}", delta=f"{est_price - curr:.2f}")
                p2.metric("預估 EPS", f"{est_eps:.2f}")
                p3.metric("預估現金股利", f"{est_dividend:.2f}")
                p4.metric("預估今年營收", f"{est_revenue/1e9:.2f} B")

            if not hist.empty:
                st.markdown("### 📈 股價走勢 (最近 6 個月)")
                st.line_chart(hist['Close'], use_container_width=True)
            else:
                st.warning("查無歷史股價走勢資料。")

        except Exception as e:
            st.error(f"分析過程錯誤: {e}")

elif menu == "💼 部位管理":
    st.subheader("💼 我的持股管理")
    st.info("此區塊目前正在建構中...")
