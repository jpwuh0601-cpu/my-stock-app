import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# 頁面設定
st.set_page_config(
    page_title="全球危機監控",
    layout="wide"
)

# 標題
st.title("🌍 全球股市危機監控 APP")

st.markdown("即時監控全球市場、VIX恐慌與AI風險")

# 股票代碼
symbols = {
    "台股加權": "^TWII",
    "道瓊工業": "^DJI",
    "NASDAQ": "^IXIC",
    "標普500": "^GSPC",
    "費城半導體": "^SOX",
    "VIX恐慌": "^VIX",
    "黃金": "GC=F"
}

# 建立欄位
cols = st.columns(len(symbols))

# 顯示數據
i = 0

for name, ticker in symbols.items():

    try:
        data = yf.Ticker(ticker).history(period="2d")

        latest = data["Close"].iloc[-1]
        previous = data["Close"].iloc[-2]

        change = latest - previous
        percent = (change / previous) * 100

        with cols[i]:
            st.metric(
                label=name,
                value=f"{latest:.2f}",
                delta=f"{change:.2f} ({percent:.2f}%)"
            )

        i += 1

    except:
        with cols[i]:
            st.error(f"{name} 讀取失敗")
        i += 1

# VIX 分析
st.subheader("🚨 市場風險分析")

try:
    vix = yf.Ticker("^VIX").history(period="1d")["Close"].iloc[-1]

    if vix < 20:
        st.success("市場情緒穩定")

    elif vix < 30:
        st.warning("市場開始出現恐慌")

    else:
        st.error("⚠️ 高風險警報：市場恐慌升高")

except:
    st.error("VIX 資料讀取失敗")

# NASDAQ 圖表
st.subheader("📈 NASDAQ 近六個月走勢")

try:
    nasdaq = yf.Ticker("^IXIC").history(period="6mo")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=nasdaq.index,
        y=nasdaq["Close"],
        mode='lines',
        name='NASDAQ'
    ))

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

except:
    st.error("NASDAQ 圖表讀取失敗")

# 防禦建議
st.subheader("🛡️ 防禦策略")

st.info("""
目前建議：

- 保持現金部位
- 注意 VIX 是否突破 30
- 留意 AI 類股修正
- 避免高槓桿股票
""")

# 更新時間
st.caption(f"更新時間：{datetime.now()}")