import streamlit as st
from analysis_utils import get_stock_analysis

st.set_page_config(page_title="股票即時分析器", layout="wide")
st.title("📈 股票即時分析器")

# 使用快取，減少重複請求，ttl=3600 代表暫存 1 小時
@st.cache_data(ttl=3600)
def cached_get_analysis(ticker):
    return get_stock_analysis(ticker)

ticker = st.text_input("請輸入股票代碼 (例如 2330)", "2330")

if st.button("開始分析"):
    with st.spinner('正在從 Yahoo Finance 抓取數據...'):
        price, sma, status, financials = cached_get_analysis(ticker)
    
    if price:
        st.subheader(f"標的: {ticker} 市場指標")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("營收(億)", financials["營收"])
        col2.metric("稅後淨利", financials["淨利"])
        col3.metric("EPS", financials["EPS"])
        col4.metric("現金股利", financials["現金股利"])
        
        st.divider()
        st.write(f"### 技術分析狀態: {status}")
        st.write(f"**最新價格:** {price:.2f} TWD")
        st.write(f"**20日均線:** {sma:.2f} TWD")
    else:
        st.error("無法取得該股票資料，請檢查代碼是否正確。")
