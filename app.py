import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI 籌碼實戰分析看板", layout="wide")

st.title("📈 互動式 AI 籌碼實戰分析")

# 側邊欄：手動輸入自選股
with st.sidebar:
    st.header("自選股設定")
    manual_ticker = st.text_input("輸入股票代號 (如 2330.TW):", value="2330.TW")
    refresh_btn = st.button("即時分析此股票")

# 分析函式
@st.cache_data(ttl=300)
def fetch_realtime_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info
    except Exception as e:
        return None

# 主邏輯
if refresh_btn or manual_ticker:
    with st.spinner(f"正在分析 {manual_ticker} 的最新籌碼與數據..."):
        info = fetch_realtime_data(manual_ticker)
        
        if info:
            # 顯示卡片
            col1, col2, col3 = st.columns(3)
            col1.metric("當前股價", f"{info.get('currentPrice', 'N/A')}")
            col2.metric("本益比 (PE)", f"{info.get('forwardPE', 'N/A')}")
            col3.metric("每股盈餘 (EPS)", f"{info.get('trailingEps', 'N/A')}")
            
            st.markdown("### 🏛️ 籌碼面數據")
            st.write(f"流通在外股數: {info.get('floatShares', 0):,}")
            
            st.markdown("### 🤖 AI 籌碼與分析觀點")
            # 這裡簡單模擬分析，實際可串接您的 analyzer.py
            analysis = f"針對 {manual_ticker} 的綜合分析：PE 為 {info.get('forwardPE', 0)}，基本面表現穩健。AI 建議：{'積極觀察' if info.get('forwardPE', 20) < 20 else '謹慎佈局'}。"
            st.info(analysis)
        else:
            st.error("無法取得該股票數據，請檢查代號是否正確 (需加上 .TW 或 .TWO)。")
else:
    st.info("請在左側輸入股票代號並點擊「即時分析此股票」開始。")
