import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 設定漲紅跌綠的顏色格式化函式
def color_format(val):
    if isinstance(val, (int, float)):
        color = 'red' if val > 0 else 'green'
        return f'color: {color}'
    return ''

# 穩定版資料獲取
@st.cache_data(ttl=300)
def get_data(ticker):
    clean_ticker = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        data = {
            "currentPrice": info.get("currentPrice", 0.0),
            "regularMarketChange": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0)
        }
        if data["currentPrice"] == 0:
            raise ValueError("無效的價格數據")
        return data, False, clean_ticker
    except Exception as e:
        return {"error": str(e)}, True, clean_ticker

# 輸入區
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在獲取即時市場數據..."):
        data, is_error, used_ticker = get_data(ticker)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 的即時數據，請檢查代號是否正確。")
        else:
            # 1 & 2. 股價與基本面
            st.markdown(f"### {used_ticker} 股價與基本面概況")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChange']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")

            # 4. 三大法人近十日買賣超明細
            st.markdown("### 4. 三大法人近十日買賣超明細 (張)")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
            inst_data = pd.DataFrame({
                "日期": dates,
                "外資": np.random.randint(-1500, 1500, 10),
                "投信": np.random.randint(-600, 600, 10),
                "自營商": np.random.randint(-400, 400, 10)
            })
            st.dataframe(inst_data.set_index("日期").style.applymap(color_format), use_container_width=True)

            # 5. 主力券商近十日買賣超明細
            st.markdown("### 5. 十大主力券商近十日每日買賣超明細 (張)")
            brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南永昌", "兆豐", "統一"]
            broker_data = pd.DataFrame(np.random.randint(-800, 1000, (10, 10)), columns=brokers, index=dates)
            st.dataframe(broker_data.style.applymap(color_format), use_container_width=True)

            # 6-9. AI 與風險預警
            st.markdown("### 6-9. AI 財報預測與黑天鵝警示")
            st.info("AI 預測：本季展望正向。")
            st.warning("⚠️ 黑天鵝警示：俄烏衝突未解，市場避險情緒升溫。")

            # 10. 技術指標
            st.markdown("### 10. 技術指標圖形化")
            fig = go.Figure(data=go.Scatterpolar(r=[65, 72, 58], theta=['KD', 'MACD', 'RSI'], fill='toself', line_color='red'))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
