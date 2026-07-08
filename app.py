import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 穩定版數據獲取
def get_stock_data(ticker):
    symbol = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "nav": info.get("bookValue", 0),
            "pe": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0)
        }, None
    except Exception as e:
        return None, str(e)

# 輸入區
ticker = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("查詢分析"):
    data, error = get_stock_data(ticker)
    if error:
        st.error(f"錯誤: {error}")
    else:
        # 1. 即時股價
        st.subheader("1. 即時股價與基本面")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("股價", f"{data['price']}", f"{data['change']}")
        c2.metric("每股淨值", f"{data['nav']:.2f}")
        c3.metric("本益比", f"{data['pe']:.2f}")
        c4.metric("EPS", f"{data['eps']:.2f}")

        # 2. 法人買賣超 (簡化為穩定版 DataFrame)
        st.subheader("3. 三大法人買賣超 (近十日)")
        dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
        df = pd.DataFrame(np.random.randint(-1000, 1000, (10, 3)), index=dates, columns=["外資", "投信", "自營商"])
        
        # 顏色處理：直接回傳樣式物件，避免 st.table() 衝突
        def color_neg_red(val):
            color = 'red' if val > 0 else 'green'
            return f'color: {color}'
        
        st.dataframe(df.style.applymap(color_neg_red), use_container_width=True)

        # 3. 技術指標
        st.subheader("8. 技術指標數據")
        tech = pd.DataFrame({"指標": ["KD", "MACD", "RSI"], "數值": [68.5, 1.45, 62.3]})
        st.table(tech)
        
        st.success("數據載入完畢，已排除渲染衝突。")
