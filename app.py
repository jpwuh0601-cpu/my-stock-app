import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# 頁面配置 (必須放在最上方，確保 UI 優先呈現)
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 模擬資料獲取 (為了保證絕不卡死，我們強制分離邏輯)
def get_stock_data(ticker):
    # 使用局部匯入，避免啟動時卡住
    import yfinance as yf
    try:
        clean_ticker = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        return {
            "price": info.get("currentPrice", 100.0),
            "change": info.get("regularMarketChangePercent", 0.0),
            "nav": info.get("bookValue", 50.0),
            "pe": info.get("trailingPE", 15.0),
            "eps": info.get("trailingEps", 5.0),
            "shares": info.get("sharesOutstanding", 1000000000)
        }, clean_ticker
    except Exception as e:
        return None, str(e)

st.title("📈 專業股市決策儀表板")

# 使用 SideBar 進行輸入，確保主介面乾淨
with st.sidebar:
    st.header("股票查詢")
    user_ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")
    submitted = st.button("查詢分析數據")

# 主頁面內容
if submitted:
    with st.spinner("正在讀取資料..."):
        data, ticker_or_error = get_stock_data(user_ticker)
        
        if data is None:
            st.error(f"查詢失敗: {ticker_or_error}")
        else:
            # 1. 核心指標面板 (並排)
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("即時股價", f"{data['price']:.2f}", f"{data['change']:.2f}%")
            col2.metric("每股淨值", f"{data['nav']:.2f}")
            col3.metric("本益比", f"{data['pe']:.2f}")
            col4.metric("EPS", f"{data['eps']:.2f}")
            col5.metric("發行股數", f"{data['shares']/1e8:.1f} 億")

            # 2. 第 9 項：財務預估模型
            st.markdown("---")
            st.subheader("📊 第 9 項：明年財務預估模型")
            c1, c2 = st.columns(2)
            margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
            payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
            
            # 計算邏輯
            est_revenue = 10000000000 * 1.15 # 模擬數據
            est_net_profit = est_revenue * margin_rate
            est_eps = est_net_profit / data['shares']
            est_div = est_eps * payout_rate
            
            p1, p2, p3, p4 = st.columns(4)
            p1.metric("預估明年營收", f"{est_revenue/1e9:.1f} 億")
            p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
            p3.metric("預估 EPS", f"{est_eps:.2f}")
            p4.metric("預估現金股利", f"{est_div:.2f}")

            # 3. 法人明細 (模擬)
            st.markdown("---")
            st.subheader("三大法人買賣超")
            dummy_df = pd.DataFrame(np.random.randint(-1000, 1000, (5, 3)), columns=["外資", "投信", "自營商"])
            st.dataframe(dummy_df.style.map(lambda x: f"color: {'red' if x > 0 else 'green'}"))
else:
    st.info("請在左側輸入股票代號並點擊「查詢分析數據」開始。")
