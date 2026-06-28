import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import yfinance as yf
from datetime import datetime

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
            
            curr = info.get('currentPrice') or info.get('regularMarketPrice', 0.0)
            eps = info.get('trailingEps', 0.0)
            pe = info.get('trailingPE', 0.0)
            bv = info.get('bookValue', 0.0)
            
            # 使用更積極的預設值，確保計算不崩潰
            shares = info.get('sharesOutstanding') or 100000000.0
            prev_revenue = info.get('totalRevenue') or 1000000000.0 

            st.markdown("### 📊 即時市場動態")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{curr:.2f}")
            col2.metric("EPS", f"{eps:.2f}")
            col3.metric("本益比", f"{pe:.2f}")
            col4.metric("每股淨值", f"{bv:.2f}")
            
            st.divider()

            st.markdown("### 🔮 明年專業推算數據 (八步驟邏輯)")
            # 將輸入參數直接展開顯示，確保即使數據抓取為 0 也能立刻修正
            with st.expander("📝 請確認或調整推算參數", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                manual_prev_revenue = c1.number_input("上年度營收 (元)", value=float(prev_revenue), step=1e7)
                yoy = c2.number_input("累積營收年增率 (%)", value=10.0) / 100
                margin = c3.number_input("稅後淨利率 (%)", value=15.0) / 100
                payout = c4.number_input("盈餘分配率 (%)", value=60.0) / 100
                
                c5, c6 = st.columns(2)
                target_pe = c5.number_input("預期本益比 (P/E)", value=float(pe) if pe and pe > 0 else 15.0)
                manual_shares = c6.number_input("發行股數", value=float(shares), step=1e6)
            
            # 推算邏輯執行
            est_revenue = manual_prev_revenue * (1 + yoy)
            est_net_profit = est_revenue * margin
            est_eps = est_net_profit / manual_shares if manual_shares > 0 else 0
            est_dividend = est_eps * payout
            est_price = est_eps * target_pe

            st.markdown("---")
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("預估明年股價", f"{est_price:.2f}")
            p2.metric("預估 EPS", f"{est_eps:.2f}")
            p3.metric("預估現金股利", f"{est_dividend:.2f}")
            p4.metric("預估今年營收", f"{est_revenue/1e9:.2f} B")

            if not hist.empty:
                st.markdown("### 📈 股價走勢")
                st.line_chart(hist['Close'], use_container_width=True)
            else:
                st.warning("查無歷史股價走勢資料。")

        except Exception as e:
            st.error(f"分析錯誤: {e}，請檢查輸入代號。")

elif menu == "💼 部位管理":
    st.subheader("💼 我的持股管理")
    st.info("此區塊目前正在建構中...")
