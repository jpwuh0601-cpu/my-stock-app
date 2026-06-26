import streamlit as st
from analysis_utils import get_stock_analysis

st.title("股票即時分析器")
ticker = st.text_input("請輸入股票代碼", "2330")

if st.button("開始分析"):
    price, sma, status, financials = get_stock_analysis(ticker)
    
    if price:
        # 並排顯示財務指標
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("營收(億)", financials["營收"])
        col2.metric("稅後淨利", financials["淨利"])
        col3.metric("EPS", financials["EPS"])
        col4.metric("現金股利", financials["現金股利"])
        
        st.divider()
        st.write(f"### 市場分析: {status}")
        st.write(f"最新價格: {price:.2f} | 20日均線: {sma:.2f}")
    else:
        st.error("無法取得數據，請確認代碼是否正確。")
