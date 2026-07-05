import streamlit as st
import yfinance as yf
import pandas as pd
import os

st.set_page_config(page_title="股票監控儀表板", layout="wide")

st.title("📊 股票籌碼與漲跌監控儀表板")

def get_tickers():
    if os.path.exists("tickers.txt"):
        with open("tickers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def get_market_data(tickers):
    data = []
    for t in tickers:
        stock = yf.Ticker(t)
        hist = stock.history(period="2d")
        if len(hist) >= 2:
            price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            change = ((price - prev_price) / prev_price) * 100
            data.append({"代號": t, "價格": round(price, 2), "漲跌幅": round(change, 2)})
    return pd.DataFrame(data)

tickers = get_tickers()
df = get_market_data(tickers)

if not df.empty:
    st.subheader("即時漲跌排行榜")
    # 設定漲跌顏色標記
    def highlight_change(val):
        color = 'red' if val > 3 else 'green' if val < -3 else 'black'
        return f'color: {color}'
    
    st.dataframe(df.style.applymap(highlight_change, subset=['漲跌幅']), use_container_width=True)

    st.divider()
    st.info("💡 漲跌幅超過 3% 或低於 -3% 將以紅色或綠色標記顯示。")
else:
    st.warning("請在 tickers.txt 中輸入有效代號。")
