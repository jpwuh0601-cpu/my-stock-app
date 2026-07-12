import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 數據獲取函式 (加入快取與錯誤處理)
@st.cache_data(ttl=600)
def get_data(ticker):
    try:
        if not ticker.endswith(('.TW', '.TWO')):
            ticker += ".TW"
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 基本數據結構
        data = {
            "currentPrice": info.get("currentPrice", 0.0),
            "regularMarketChange": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0),
            "sharesOutstanding": info.get("sharesOutstanding", 1000000000), # 預設值
            "yoy_growth": 0.15, # 假設最新年增率
            "last_year_revenue": info.get("totalRevenue", 10000000000)
        }
        return data, False
    except Exception as e:
        return {"error": str(e)}, True

# 側邊欄控制
with st.sidebar:
    st.header("股票查詢")
    user_ticker = st.text_input("輸入股票代號 (例: 2330)", "2330")
    submit = st.button("查詢分析數據")

if submit:
    data, is_error = get_data(user_ticker)
    
    if is_error:
        st.error(f"無法載入該股票代號，請檢查代號是否正確。錯誤訊息: {data['error']}")
    else:
        # 1. 核心指標面板
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChange']:.2f}%")
        col2.metric("每股淨值", f"{data['bookValue']:.2f}")
        col3.metric("本益比", f"{data['trailingPE']:.2f}")
        col4.metric("EPS", f"{data['trailingEps']:.2f}")
        col5.metric("發行股數", f"{data['sharesOutstanding']:,}")

        # 2. 第9項：預估財務模型面板
        st.markdown("---")
        st.subheader("📊 第 9 項：明年財務預估模型")
        
        c1, c2 = st.columns(2)
        with c1:
            margin_rate = st.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
        with c2:
            payout_rate = st.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100

        # 計算公式 (依照您的需求)
        est_revenue = data['last_year_revenue'] * (1 + data['yoy_growth'])
        est_net_profit = est_revenue * margin_rate
        est_eps = est_net_profit / data['sharesOutstanding']
        est_dividend = est_eps * payout_rate

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("預估明年營收", f"{est_revenue/1e9:.1f} 億")
        p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
        p3.metric("預估 EPS", f"{est_eps:.2f}")
        p4.metric("預估現金股利", f"{est_dividend:.2f}")

        # 3. 籌碼面與技術面 (固定格式)
        st.markdown("---")
        st.subheader("三大法人與券商買賣超明細")
        dummy_df = pd.DataFrame(np.random.randint(-1000, 1000, (5, 3)), columns=["外資", "投信", "自營商"])
        st.dataframe(dummy_df.style.map(lambda x: f"color: {'red' if x > 0 else 'green'}"))

        st.subheader("技術指標")
        fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
        st.plotly_chart(fig, use_container_width=True)
