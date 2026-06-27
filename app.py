import streamlit as st
from analysis_utils import get_stock_analysis
from ai_engine import get_ai_summary

# 設定頁面寬度
st.set_page_config(page_title="專業股市 AI 決策系統", layout="wide")

st.title("📊 專業股市 AI 決策系統")

# 初始化 session_state，確保資料不會因為重整而消失
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = None

# 使用快取，減少重複請求，ttl=3600 (1小時)
@st.cache_data(ttl=3600)
def cached_analysis(ticker):
    return get_stock_analysis(ticker)

ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")

if st.button("查詢分析"):
    with st.spinner('正在從 Yahoo Finance 抓取數據...'):
        # 執行分析並存入 session_state
        st.session_state.analysis_data = cached_analysis(ticker)
        # 每次重新查詢時，清除舊的 AI 分析結果
        st.session_state.ai_summary = None

# 顯示資料
if st.session_state.analysis_data:
    price, sma, status, data = st.session_state.analysis_data
    
    if price:
        st.subheader(f"標的: {ticker} 關鍵指標")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時報價", f"{data['現價']:.2f}")
        col2.metric("漲跌幅", data['漲跌幅'])
        col3.metric("EPS", data['EPS'])
        
        col4, col5, col6 = st.columns(3)
        col4.metric("本益比", data['本益比'])
        col5.metric("每股淨值", data['每股淨值'])
        col6.metric("發行股數", f"{data['發行股數']:,}")
        
        st.divider()
        st.write(f"### 趨勢狀態: {status} (20日均線: {sma:.2f})")
        
        # AI 深度分析區塊
        st.divider()
        st.subheader("🤖 AI 深度解讀")
        
        if st.button("點擊產生 AI 分析建議"):
            with st.spinner('AI 正在分析市場數據...'):
                st.session_state.ai_summary = get_ai_summary(data)
                
        if st.session_state.ai_summary:
            st.markdown(st.session_state.ai_summary)
    else:
        st.error("無法取得該股票資料，請檢查代號是否正確。")
