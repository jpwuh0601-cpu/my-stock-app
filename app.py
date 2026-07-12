import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go

# -----------------------
# 頁面設定
# -----------------------
st.set_page_config(
    page_title="專業股市決策儀表板",
    layout="wide"
)

st.title("📈 專業股市決策儀表板")

# -----------------------
# 自動判斷上市/上櫃
# -----------------------
@st.cache_data(ttl=3600)
def get_stock_symbol(code):

    if code.endswith(".TW") or code.endswith(".TWO"):
        return code

    for suffix in [".TW", ".TWO"]:
        try:
            test = yf.Ticker(code + suffix)
            hist = test.history(period="1d")

            if not hist.empty:
                return code + suffix
        except:
            pass

    return code + ".TW"


# -----------------------
# 股票資料
# -----------------------
@st.cache_data(ttl=600)
def get_data(code):

    ticker = get_stock_symbol(code)

    stock = yf.Ticker(ticker)

    info = stock.info

    data = {
        "ticker": ticker,
        "currentPrice": info.get("currentPrice", 0),
        "regularMarketChange":
            info.get("regularMarketChangePercent", 0),

        "bookValue": info.get("bookValue", 0),
        "trailingPE": info.get("trailingPE", 0),
        "trailingEps": info.get("trailingEps", 0),

        "sharesOutstanding":
            info.get("sharesOutstanding", 0),

        "last_year_revenue":
            info.get("totalRevenue", 0),

        "yoy_growth": 0.15
    }

    hist = stock.history(period="6mo")

    return data, hist


# -----------------------
# 側邊欄
# -----------------------
with st.sidebar:

    st.header("股票查詢")

    user_ticker = st.text_input(
        "輸入股票代號",
        "2330"
    )

    submit = st.button("查詢分析")


# -----------------------
# 主畫面
# -----------------------
if submit:

    try:

        data, hist = get_data(user_ticker)

        # -----------------------
        # 核心指標
        # -----------------------
        st.subheader("📊 核心財務指標")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "即時股價",
            f"{data['currentPrice']:.2f}",
            f"{data['regularMarketChange']:.2f}%"
        )

        col2.metric(
            "每股淨值",
            f"{data['bookValue']:.2f}"
        )

        col3.metric(
            "本益比",
            f"{data['trailingPE']:.2f}"
        )

        col4.metric(
            "EPS",
            f"{data['trailingEps']:.2f}"
        )

        col5.metric(
            "發行股數",
            f"{data['sharesOutstanding']/1e8:.2f} 億股"
        )

        st.divider()

        # -----------------------
        # K線圖
        # -----------------------
        st.subheader("📉 K線圖分析")

        hist["MA5"] = hist["Close"].rolling(5).mean()
        hist["MA20"] = hist["Close"].rolling(20).mean()
        hist["MA60"] = hist["Close"].rolling(60).mean()

        fig = go.Figure()

        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
                name="K線"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MA5"],
                name="MA5"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MA20"],
                name="MA20"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=hist["MA60"],
                name="MA60"
            )
        )

        fig.update_layout(
            height=700,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # -----------------------
        # 財務預估模型
        # -----------------------
        st.subheader("📊 AI 明年財務預估模型")

        c1, c2 = st.columns(2)

        with c1:
            margin_rate = st.slider(
                "預估稅後淨利率(%)",
                5.0,
                30.0,
                15.0
            ) / 100

        with c2:
            payout_rate = st.slider(
                "預估配息率(%)",
                30.0,
                90.0,
                60.0
            ) / 100

        est_revenue = (
            data["last_year_revenue"] *
            (1 + data["yoy_growth"])
        )

        est_profit = est_revenue * margin_rate

        est_eps = (
            est_profit /
            data["sharesOutstanding"]
        )

        est_dividend = est_eps * payout_rate

        p1, p2, p3, p4 = st.columns(4)

        p1.metric(
            "預估明年營收",
            f"{est_revenue/1e8:.2f} 億元"
        )

        p2.metric(
            "預估稅後淨利",
            f"{est_profit/1e8:.2f} 億元"
        )

        p3.metric(
            "預估 EPS",
            f"{est_eps:.2f}"
        )

        p4.metric(
            "預估現金股利",
            f"{est_dividend:.2f}"
        )

        st.divider()

        # -----------------------
        # 法人買賣超
        # -----------------------
        st.subheader("🏦 三大法人買賣超")

        dummy_df = pd.DataFrame(
            np.random.randint(
                -1000,
                1000,
                (10, 3)
            ),
            columns=[
                "外資",
                "投信",
                "自營商"
            ]
        )

        def color_positive(v):
            if v > 0:
                return "color:red"
            elif v < 0:
                return "color:green"
            return ""

        st.dataframe(
            dummy_df.style.map(color_positive)
        )

        st.divider()

        # -----------------------
        # 技術分析雷達圖
        # -----------------------
        st.subheader("📡 技術分析")

        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=[70, 65, 60, 75, 55],
                theta=[
                    "KD",
                    "RSI",
                    "MACD",
                    "均線",
                    "成交量"
                ],
                fill="toself"
            )
        )

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0,100]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

        st.divider()

        # -----------------------
        # AI風險警示
        # -----------------------
        st.subheader("⚠️ AI 風險警示")

        if data["trailingPE"] > 30:
            st.error(
                "🔴 本益比偏高，投資風險較高"
            )

        elif data["trailingPE"] > 20:
            st.warning(
                "🟡 本益比略高，建議觀察"
            )

        else:
            st.success(
                "🟢 本益比合理"
            )

    except Exception as e:

        st.error(
            f"資料讀取失敗：{e}"
        )
