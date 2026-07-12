import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 必須放在最前方的配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 將數據邏輯封裝並使用懶加載
def get_stock_data(ticker):
    import yfinance as yf
    try:
        # 自動處理 TW 代號
        symbol = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
        stock = yf.Ticker(symbol)
        info = stock.info
        
        return {
            "price": info.get("currentPrice", 0.0),
            "change": info.get("regularMarketChangePercent", 0.0) * 100,
            "nav": info.get("bookValue", 0.0),
            "pe": info.get("trailingPE", 0.0),
            "eps": info.get("trailingEps", 0.0),
            "shares": info.get("sharesOutstanding", 1000000000),
            "last_year_revenue": 9000000000,
            "yoy_growth": 0.15
        }, symbol
    except Exception as e:
        return None, str(e)

st.title("📈 專業股市決策儀表板")

# 穩定輸入區
with st.sidebar:
    st.header("股票查詢")
    user_ticker = st.text_input("輸入股票代號 (例: 2330)", "2330")
    btn_run = st.button("查詢分析")

if btn_run:
    with st.spinner("正在安全連線獲取數據..."):
        data, ticker_res = get_stock_data(user_ticker)
        
        if not data:
            st.error(f"無法獲取資料: {ticker_res}")
        else:
            # 核心數值顯示
            cols = st.columns(5)
            cols[0].metric("股價", f"{data['price']:.2f}", f"{data['change']:.2f}%")
            cols[1].metric("每股淨值", f"{data['nav']:.2f}")
            cols[2].metric("本益比", f"{data['pe']:.2f}")
            cols[3].metric("EPS", f"{data['eps']:.2f}")
            cols[4].metric("發行股數", f"{data['shares']/1e8:.1f} 億")

            # 財務預估模型
            st.subheader("📊 財務預估面板")
            c1, c2 = st.columns(2)
            margin = c1.slider("稅後淨利率 (%)", 5, 30, 15) / 100
            payout = c2.slider("盈餘分配率 (%)", 30, 90, 60) / 100
            
            est_rev = data['last_year_revenue'] * (1 + data['yoy_growth'])
            est_net = est_rev * margin
            est_eps = est_net / data['shares']
            
            p_cols = st.columns(4)
            p_cols[0].metric("預估營收", f"{est_rev/1e9:.1f} 億")
            p_cols[1].metric("預估淨利", f"{est_net/1e8:.1f} 億")
            p_cols[2].metric("預估 EPS", f"{est_eps:.2f}")
            p_cols[3].metric("預估股利", f"{(est_eps * payout):.2f}")
            
            st.success("數據讀取成功！")
else:
    st.info("請在側邊欄輸入代號並點擊查詢。")
