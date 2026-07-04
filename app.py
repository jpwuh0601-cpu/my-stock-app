import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

st.title("股票分析應用 (優化版)")

# 獲取使用者輸入
ticker = st.text_input("輸入股票代號 (例如 2330.TW)", "2330.TW")

# 使用快取函式來獲取數據，避免觸發 Rate Limit
@st.cache_data(ttl=3600)  # 每小時更新一次快取
def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    # 加入簡單的重試邏輯
    for i in range(3):
        try:
            return stock.history(period="1mo")
        except Exception:
            time.sleep(2)  # 如果失敗，等待 2 秒再重試
    return None

if st.button("執行分析"):
    with st.spinner('正在從 Yahoo Finance 獲取數據...'):
        hist = get_stock_data(ticker)
        
        if hist is not None and not hist.empty:
            # 繪製走勢圖
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index, 
                open=hist['Open'], 
                high=hist['High'], 
                low=hist['Low'], 
                close=hist['Close']
            )])
            fig.update_layout(title=f"{ticker} 近一個月走勢", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("無法取得數據，請確認代號是否正確，或稍後再試 (目前已被 Yahoo 限制流量)。")

st.info("提示：若發生 Error，請等待約 10-15 分鐘後再重新整理頁面。")
