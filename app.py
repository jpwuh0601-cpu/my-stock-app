import streamlit as st
import yfinance as yf
import plotly.express as px
import time

st.set_page_config(layout="wide", page_title="金融即時查詢終端")
st.title("📊 金融即時查詢終端")

# 側邊欄說明
st.sidebar.info("請在下方輸入完整股票代號 (例如: 2330.TW)")

# 手動輸入區域
ticker_input = st.text_input("輸入股票代號", placeholder="例如: 2330.TW")
search_btn = st.button("取得即時數據")

if search_btn and ticker_input:
    with st.spinner(f"正在查詢 {ticker_input}..."):
        try:
            # 增加隨機延遲，降低被 Yahoo 封鎖機率
            time.sleep(1)
            
            ticker = yf.Ticker(ticker_input)
            hist = ticker.history(period="1mo")
            
            if hist.empty:
                st.error("查無此股票，請確認代號是否正確（台股需加上 .TW）。")
            else:
                # 抓取基本數據
                info = ticker.info
                current_price = info.get("currentPrice") or hist['Close'].iloc[-1]
                
                # 顯示面板
                c1, c2, c3 = st.columns(3)
                c1.metric("目前股價", f"{current_price:.2f}")
                c2.metric("本益比", f"{info.get('forwardPE', 0):.2f}")
                c3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                
                # 繪圖
                fig = px.line(hist, y="Close", title=f"{ticker_input} 近期走勢")
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"查詢失敗: {e}")
            st.warning("若持續失敗，可能是因為請求頻率過高。請稍候幾分鐘再試。")
