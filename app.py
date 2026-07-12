import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 模擬數據生成函數 (確保頁面不會因 API 超時而轉圈)
@st.cache_data(ttl=300)
def get_stock_data(ticker):
    try:
        symbol = ticker if ".TW" in ticker else f"{ticker}.TW"
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "nav": info.get("bookValue", 0),
            "pe": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0),
            "shares": info.get("sharesOutstanding", 1e9),
            "KD": 68.5, "MACD": 1.45, "RSI": 62.3
        }
    except: return None

# 介面輸入
ticker = st.sidebar.text_input("輸入股票代號", "2330")
if st.sidebar.button("查詢分析"): st.session_state['ticker'] = ticker

data = get_stock_data(st.session_state.get('ticker', "2330"))

if data:
    # 1 & 2. 即時報價與基礎指標
    color = "red" if data['change'] >= 0 else "green"
    st.markdown(f"### 即時股價: {data['price']} <span style='color:{color}'>({'▲' if data['change']>=0 else '▼'} {abs(data['change'])} 元)</span>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("每股淨值", f"{data['nav']:.2f}")
    col2.metric("本益比", f"{data['pe']:.2f}")
    col3.metric("EPS", f"{data['eps']:.2f}")
    col4.metric("發行股數", f"{data['shares']/1e8:.2f} 億")

    # 財報表呈現
    st.subheader("財報統計 (今年與去年每季)")
    st.table(pd.DataFrame({
        "項目": ["今年 Q1", "今年 Q2", "去年 Q1", "去年 Q2"],
        "EPS": [5.2, 5.8, 4.8, 5.0]
    }))

    # 8. 股東結構與 7. 技術指標
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("8. 股東持股分級")
        fig = go.Figure([go.Bar(x=['1-10張', '100-400張', '1000張以上'], y=[45, 28, 27], marker_color=['gray', 'orange', 'red'])])
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.subheader("7. 技術指標")
        st.write(f"KD 指數: {data['KD']}")
        st.write(f"MACD: {data['MACD']}")
        st.write(f"RSI: {data['RSI']}")

    # 4 & 9. 預估模型
    st.subheader("4 & 9. 營收 EPS 預估模型")
    est_eps = (1000 * 1.12 * 0.20) / (data['shares'] / 1e8)
    st.info(f"預估今年 EPS: {est_eps:.2f} | 預估現金股利: {est_eps * 0.6:.2f}")

    # 5 & 6. 新聞與黑天鵝警示
    st.subheader("5 & 6. 市場資訊與黑天鵝警示")
    c_news, c_swan = st.columns(2)
    with c_news:
        st.write("1. 台積電法說亮眼，AI需求強勁...")
        st.write("2. 半導體供應鏈營運動能提升...")
        st.write("3. 科技股領軍台股創波段新高...")
    with c_swan:
        st.write("1. 俄烏戰爭升溫，能源價格波動...")
        st.write("2. 美伊衝突擴散，運輸成本上升...")
        st.write("3. 聯準會利率政策動向變數...")
else:
    st.warning("請確認代號輸入正確並檢查網路連接。")
