import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AI台股投資決策平台",
    layout="wide"
)

st.title("📈 AI台股投資決策平台")

FINMIND_TOKEN = st.secrets["FINMIND_TOKEN"]

# ===============================
# FinMind API
# ===============================

BASE_URL = "https://api.finmindtrade.com/api/v4/data"

headers = {
    "Authorization": f"Bearer {FINMIND_TOKEN}"
}

ticker = st.text_input(
    "請輸入股票代號",
    value="2330"
)

# ===============================
# 股價資料
# ===============================

@st.cache_data(ttl=3600)
def get_stock_price(stock_id):

    start_date = (
        datetime.today() - timedelta(days=365)
    ).strftime("%Y-%m-%d")

    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": start_date,
        "token": FINMIND_TOKEN
    }

    r = requests.get(
        BASE_URL,
        params=params
    )

    data = r.json()["data"]

    return pd.DataFrame(data)

price_df = get_stock_price(ticker)

if price_df.empty:
    st.error("查無股票資料")
    st.stop()

latest = price_df.iloc[-1]

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "收盤價",
        latest["close"]
    )

with col2:
    st.metric(
        "最高價",
        latest["max"]
    )

with col3:
    st.metric(
        "最低價",
        latest["min"]
    )

with col4:
    st.metric(
        "成交量",
        f"{latest['Trading_Volume']:,}"
    )

# ===============================
# K線圖
# ===============================

fig = go.Figure(
    data=[
        go.Candlestick(
            x=price_df["date"],
            open=price_df["open"],
            high=price_df["max"],
            low=price_df["min"],
            close=price_df["close"]
        )
    ]
)

fig.update_layout(
    title=f"{ticker} K線圖",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===============================
# 三大法人
# ===============================

@st.cache_data(ttl=3600)
def get_institution(stock_id):

    start_date = (
        datetime.today()-timedelta(days=20)
    ).strftime("%Y-%m-%d")

    params = {
        "dataset":
        "TaiwanStockInstitutionalInvestorsBuySell",
        "data_id":stock_id,
        "start_date":start_date,
        "token":FINMIND_TOKEN
    }

    r=requests.get(
        BASE_URL,
        params=params
    )

    return pd.DataFrame(
        r.json()["data"]
    )

inst_df=get_institution(ticker)

st.subheader("三大法人近十日買賣超")

st.dataframe(
    inst_df.tail(10),
    use_container_width=True
)

# ===============================
# 月營收
# ===============================

@st.cache_data(ttl=3600)
def get_revenue(stock_id):

    params={
        "dataset":"TaiwanStockMonthRevenue",
        "data_id":stock_id,
        "start_date":"2024-01-01",
        "token":FINMIND_TOKEN
    }

    r=requests.get(
        BASE_URL,
        params=params
    )

    return pd.DataFrame(
        r.json()["data"]
    )

rev_df=get_revenue(ticker)

st.subheader("月營收")

st.dataframe(
    rev_df.tail(12),
    use_container_width=True
)

# ===============================
# 財務指標
# ===============================

revenue_growth = (
    rev_df.iloc[-1]["revenue"] /
    rev_df.iloc[-13]["revenue"] - 1
)

assume_margin = 0.18
assume_share = 25930000000
assume_payout = 0.65

est_revenue = (
    rev_df["revenue"].tail(12).sum()
    * (1 + revenue_growth)
)

est_profit = (
    est_revenue * assume_margin
)

est_eps = (
    est_profit / assume_share
)

est_dividend = (
    est_eps * assume_payout
)

st.subheader("AI財報預估")

c1,c2,c3=st.columns(3)

c1.metric(
    "預估EPS",
    round(est_eps,2)
)

c2.metric(
    "預估股利",
    round(est_dividend,2)
)

c3.metric(
    "營收成長率",
    f"{revenue_growth*100:.2f}%"
)
