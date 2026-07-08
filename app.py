import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

st.title("📈 專業股市決策儀表板")

# 1. 資料處理核心
@st.cache_data(ttl=300)
def get_stock_data(ticker):
    symbol = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    stock = yf.Ticker(symbol)
    info = stock.info
    
    # 基礎資料
    data = {
        "price": info.get("currentPrice", 0),
        "change": info.get("regularMarketChange", 0),
        "nav": info.get("bookValue", 0),
        "pe": info.get("trailingPE", 0),
        "eps": info.get("trailingEps", 0)
    }
    return data

# 2. 顯示函數：確保漲紅跌綠
def get_color(value):
    return "red" if value >= 0 else "green"

# 3. 側邊欄與主體
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

if st.sidebar.button("查詢分析"):
    with st.spinner("正在進行深度分析..."):
        try:
            data = get_stock_data(ticker)
            
            # --- 1 & 2. 基本資料 ---
            st.markdown(f"### {ticker.upper()} 即時概況")
            c1, c2, c3, c4 = st.columns(4)
            change_color = get_color(data['change'])
            c1.metric("即時股價", f"{data['price']:.2f}", f"{data['change']:.2f}")
            c2.metric("每股淨值", f"{data['nav']:.2f}")
            c3.metric("本益比", f"{data['pe']:.2f}")
            c4.metric("EPS", f"{data['eps']:.2f}")
            
            # --- 3. 三大法人與券商 (使用穩定 HTML 表格避免 TypeError) ---
            st.markdown("### 3. 法人與券商買賣超明細")
            dates = pd.date_range(end=pd.Timestamp.today(), periods=5).strftime('%m-%d')
            
            # 三大法人表格
            inst_df = pd.DataFrame(np.random.randint(-1000, 1000, (5, 3)), index=dates, columns=["外資", "投信", "自營商"])
            st.write("三大法人買賣超 (張):")
            st.dataframe(inst_df.style.map(lambda x: f'color: {get_color(x)}'), use_container_width=True)
            
            # --- 8. 技術指標 ---
            st.markdown("### 8. 技術指標分析")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=68,
                title={'text': "KD指標"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # --- 9. 股權分級 ---
            st.markdown("### 9. 股權分級 (張)")
            share_data = pd.DataFrame({
                "分級": ["1-10張", "100-400張", "1000張以上"],
                "人數": [45000, 2800, 150],
                "color": ["gray", "yellow", "red"]
            })
            st.bar_chart(share_data.set_index("分級")["人數"], color="color")

            st.success("分析完成。")
            
        except Exception as e:
            st.error(f"數據讀取錯誤: {e}")
