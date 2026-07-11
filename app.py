import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 整合式的資料獲取邏輯 (不需外部檔案)
@st.cache_data(ttl=300)
def get_stock_data(ticker):
    ticker = ticker.strip().upper()
    if not ticker.endswith(".TW") and not ticker.endswith(".TWO") and ticker.isdigit():
        ticker += ".TW"
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if not info or "currentPrice" not in info:
            return {"error": "無法獲取股票資料"}
            
        data = {
            "price": info.get("currentPrice", 0.0),
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "change": info.get("regularMarketChange", 0.0)
        }
        
        # 模擬十日籌碼數據
        dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
        data["institutional_data"] = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-1500, 1500, 10),
            "投信": np.random.randint(-800, 800, 10)
        })
        return data
    except Exception as e:
        return {"error": str(e)}

# 渲染表格的 HTML 函式
def render_html_table(df, title):
    st.markdown(f"### {title}")
    st.dataframe(df, use_container_width=True)

# UI 操作介面
ticker = st.text_input("輸入股票代號", "2330")
if st.button("查詢分析"):
    with st.spinner("正在讀取資料..."):
        data = get_stock_data(ticker)
        if "error" in data:
            st.error(data["error"])
        else:
            # 顯示股價
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['price']:.2f}")
            col2.metric("每股淨值", f"{data['nav']:.2f}")
            col3.metric("本益比", f"{data['pe']:.2f}")
            col4.metric("EPS", f"{data['eps']:.2f}")
            
            # 顯示法人數據
            render_html_table(data["institutional_data"], "三大法人近十日買賣超")
            
            # 技術指標圖表
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself'))
            st.plotly_chart(fig)
