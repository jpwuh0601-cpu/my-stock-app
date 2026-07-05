import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI 籌碼分析看板", layout="wide")

st.title("📈 互動式 AI 籌碼實戰分析")

# 自動補全代號邏輯
def format_ticker(ticker_input):
    ticker = ticker_input.strip()
    # 如果沒有包含 .TW 或 .TWO，自動幫使用者加上
    if not any(x in ticker for x in [".TW", ".TWO"]):
        # 簡單判斷：若代號為 4 碼通常為上市，若無則依使用者輸入
        return f"{ticker}.TW"
    return ticker

@st.cache_data(ttl=600)
def fetch_stock_data(ticker):
    try:
        # 強制使用 format_ticker 處理輸入
        formatted_ticker = format_ticker(ticker)
        stock = yf.Ticker(formatted_ticker)
        info = stock.info
        if 'currentPrice' not in info:
            return None, formatted_ticker
        return info, formatted_ticker
    except Exception:
        return None, ticker

# UI 佈局
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
            st.info(f"分析標的: {ticker_used}\n\n基本面數據顯示運作正常。AI 建議：請參考上方籌碼與財務指標進行決策。")
        else:
            st.error(f"❌ 無法取得 {manual_ticker} 資料。請確認代號是否正確，或檢查是否為未上市/其他特殊代號。")
