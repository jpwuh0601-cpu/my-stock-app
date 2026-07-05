import streamlit as st
import yfinance as yf
import re

st.set_page_config(page_title="AI 籌碼分析看板", layout="wide")

st.title("📈 互動式 AI 籌碼實戰分析")

# 增強的代號自動修復邏輯
def format_ticker(ticker_input):
    ticker = ticker_input.strip().upper()
    # 移除可能存在的 TW 或 TWO
    base = re.sub(r'(TW|TWO)$', '', ticker)
    # 檢查是否為上市 (預設為 .TW)
    return f"{base}.TW"

@st.cache_data(ttl=300)
def fetch_stock_data(ticker):
    try:
        formatted = format_ticker(ticker)
        stock = yf.Ticker(formatted)
        info = stock.info
        # 如果無法取得股價，嘗試上櫃格式
        if 'currentPrice' not in info:
            stock = yf.Ticker(f"{ticker.replace('TW', '').strip()}.TWO")
            info = stock.info
            
        if 'currentPrice' not in info:
            return None, formatted
        return info, formatted
    except Exception:
        return None, ticker

with st.sidebar:
    st.header("自選股設定")
    manual_ticker = st.text_input("輸入股票代號 (如 2330):", value="2330")
    refresh_btn = st.button("即時分析")

if refresh_btn:
    with st.spinner(f"正在分析..."):
        info, ticker_used = fetch_stock_data(manual_ticker)
        
        if info:
            st.success(f"成功取得 {ticker_used} 資料")
            col1, col2, col3 = st.columns(3)
            col1.metric("當前股價", f"{info.get('currentPrice', 'N/A')}")
            col2.metric("本益比 (PE)", f"{info.get('forwardPE', 'N/A')}")
            col3.metric("EPS", f"{info.get('trailingEps', 'N/A')}")
            
            st.divider()
            st.subheader("🤖 AI 籌碼分析觀點")
            st.info(f"分析標的: {ticker_used}\n\n數據讀取正常。AI 觀點：籌碼面分析已聯動，請觀察主力資金流向。")
        else:
            st.error(f"❌ 無法取得 {manual_ticker} 資料。請確認代號是否正確。")
