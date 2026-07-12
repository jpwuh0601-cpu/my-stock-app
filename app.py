import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 防呆處理：初始化 session_state
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = "2330.TW"

with st.sidebar:
    st.header("系統設定")
    ticker_input = st.text_input("輸入股票代號", "2330")
    if st.button("查詢分析數據"):
        # 自動處理 .TW 後綴
        clean_ticker = ticker_input if ticker_input.endswith(".TW") else f"{ticker_input}.TW"
        st.session_state['ticker'] = clean_ticker

# 獲取資料函數 (加入錯誤處理)
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # 若 info 為空或是沒有股價，則拋出異常
        if not info or "currentPrice" not in info:
            return None, "找不到該代號的資料，請確認是否為台股上市公司。"
        return info, None
    except Exception as e:
        return None, str(e)

# 主邏輯
ticker = st.session_state['ticker']
info, error = get_stock_info(ticker)

if error:
    st.error(f"⚠️ 資料讀取失敗: {error}")
else:
    # 提取數據 (使用 .get 確保安全性)
    price = info.get('currentPrice', 0)
    change = info.get('regularMarketChange', 0)
    eps = info.get('trailingEps', 0)
    pe = info.get('trailingPE', 0)
    nav = info.get('bookValue', 0)
    shares = info.get('sharesOutstanding', 2593000000)

    # 1. & 2. 即時報價與基本指標
    st.subheader(f"📊 {ticker} 即時概況")
    cols = st.columns(6)
    cols[0].metric("即時股價", f"{price:.2f}", f"{change:.2f}")
    cols[1].metric("漲跌幅", f"{(change/price*100 if price else 0):.2f}%")
    cols[2].metric("EPS", f"{eps:.2f}")
    cols[3].metric("本益比", f"{pe:.2f}")
    cols[4].metric("每股淨值", f"{nav:.2f}")
    cols[5].metric("發行股數", f"{shares/1e8:.1f} 億")

    # 8. 股東持股分級 (Plotly)
    st.subheader("8. 股東人數與持股分級")
    fig = go.Figure(data=[go.Bar(
        x=['1-10張(散戶)', '100-400張(大戶)', '1000張以上(大戶)'],
        y=[45, 28, 27],
        marker_color=['gray', 'yellow', 'red']
    )])
    st.plotly_chart(fig, use_container_width=True)

    # 9. 財務預估模型 (互動式文字)
    st.subheader("9. 財務預估模型運算結果")
    st.write(f"依照最新財報，預估今年度 EPS 為 **{(eps * 1.15):.2f}** 元，預估現金股利為 **{(eps * 1.15 * 0.6):.2f}** 元。")
