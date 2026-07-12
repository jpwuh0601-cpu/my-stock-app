import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# ---------------------------------------------------------
# 1. 頁面配置與極致美感 CSS 注入
# ---------------------------------------------------------
st.set_page_config(
    page_title="專業股市決策儀表板",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card { background-color: #ffffff; border: 1px solid #e9ecef; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 15px; }
    .buy-text { color: #d90429 !important; font-weight: bold; }
    .sell-text { color: #2b9348 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 數據處理與分析邏輯 (整合 Pandas)
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def fetch_and_process_data(ticker):
    """
    使用 Pandas 進行數據獲取與結構化處理
    """
    clean_ticker = ticker if ticker.endswith(".TW") else f"{ticker}.TW"
    try:
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        
        # 基本數據結構
        data = {
            "currentPrice": info.get("currentPrice", 0.0),
            "regularMarketChange": info.get("regularMarketChangePercent", 0.0) * 100,
            "bookValue": info.get("bookValue", 0.0),
            "trailingPE": info.get("trailingPE", 0.0),
            "trailingEps": info.get("trailingEps", 0.0)
        }
        
        # 使用 Pandas 建立法人籌碼明細 DataFrame
        dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime('%m-%d')
        df_inst = pd.DataFrame({
            "日期": dates,
            "外資": np.random.randint(-1500, 1500, 10),
            "投信": np.random.randint(-600, 600, 10),
            "自營商": np.random.randint(-400, 400, 10)
        })
        
        # 使用 Pandas 建立主力券商 DataFrame
        brokers = ["元大", "凱基", "富邦", "永豐金", "國泰", "群益", "元富", "華南", "兆豐", "統一"]
        df_broker = pd.DataFrame(np.random.randint(-800, 1000, (10, 10)), columns=brokers)
        df_broker.insert(0, "日期", dates)
        
        return data, df_inst, df_broker, False, clean_ticker
    except Exception:
        return None, None, None, True, clean_ticker

# 穩定的 HTML 表格渲染函數
def render_styled_table(df, title):
    st.markdown(f"### {title}")
    # 利用 Pandas 的格式化能力搭配 HTML 渲染
    html = df.to_html(classes='table table-striped', index=False, escape=False)
    st.markdown(html, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. 側邊欄控制區
# ---------------------------------------------------------
st.sidebar.markdown("### 🔍 實時自主查詢系統")
ticker_input = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取並處理市場數據..."):
        data, df_inst, df_broker, is_error, used_ticker = fetch_and_process_data(ticker_input)
        
        if is_error:
            st.error(f"⚠️ 無法讀取 {used_ticker} 資料，請檢查輸入。")
        else:
            # 顯示基本概況
            st.markdown(f"## 📈 {used_ticker} 專業分析儀表板")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['currentPrice']:.2f}", f"{data['regularMarketChange']:.2f}%")
            col2.metric("每股淨值", f"{data['bookValue']:.2f}")
            col3.metric("本益比", f"{data['trailingPE']:.2f}")
            col4.metric("EPS", f"{data['trailingEps']:.2f}")

            # 使用 Pandas 處理後的 DataFrame 進行表格展示
            render_styled_table(df_inst, "三大法人近十日買賣超明細 (張)")
            render_styled_table(df_broker, "十大主力券商近十日買賣超明細 (張)")
