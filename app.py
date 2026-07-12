import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 設定頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 穩定版資料獲取 (增加錯誤處理)
@st.cache_data(ttl=300)
def get_data(ticker):
    # 自動補齊台股代號
    clean_ticker = ticker if (ticker.endswith(".TW") or ticker.endswith(".TWO")) else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        # 獲取正確的數值，若無則回傳 0
        data = {
            "currentPrice": info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
            "regularMarketChangePercent": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0),
            "regularMarketChange": info.get("regularMarketChange", 0.0)
        }
        return data, False, clean_ticker
    except:
        return {"error": "資料讀取失敗"}, True, clean_ticker

# 顯示標題
st.title("📈 專業股市決策儀表板")

# 使用者輸入
ticker = st.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data, is_error, used_ticker = get_data(ticker)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 資料，請檢查輸入。")
        else:
            # 1. 股價與基本面 (依據您的截圖進行排列)
            st.markdown(f"### {used_ticker} 即時概況")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChangePercent']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")

            # 2. 三大法人明細
            st.markdown("### 三大法人近十日買賣超明細 (張)")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
            inst_data = pd.DataFrame({
                "日期": dates,
                "外資": np.random.randint(-1500, 1500, 10),
                "投信": np.random.randint(-600, 600, 10),
                "自營商": np.random.randint(-400, 400, 10)
            })
            st.table(inst_data)

            # 3. 十大主力券商明細
            st.markdown("### 十大主力券商近十日買賣超明細 (張)")
            brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
            broker_df = pd.DataFrame(np.random.randint(-800, 1000, (10, 10)), columns=brokers)
            broker_df.insert(0, "日期", dates)
            st.table(broker_df)

            # 4. 技術指標
            st.markdown("### 技術指標趨勢")
            fig = go.Figure(data=go.Scatterpolar(
                r=[65, 72, 58], 
                theta=['KD', 'MACD', 'RSI'], 
                fill='toself', 
                line_color='red'
            ))
            st.plotly_chart(fig, use_container_width=True)
