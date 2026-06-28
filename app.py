import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.sidebar.title("AI 決策中樞")
page = st.sidebar.radio("功能導航", ["Daily Stock Analysis", "投資復盤日記", "自動新聞讀取"])

if page == "Daily Stock Analysis":
    st.title("Daily Stock Analysis")
    ticker_symbol = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.button("抓取最新數據與分析"):
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            # 顯示財務指標看板
            col1, col2, col3 = st.columns(3)
            col1.metric("本益比 (PE)", f"{info.get('trailingPE', 'N/A')}")
            col2.metric("殖利率", f"{info.get('dividendYield', 0)*100:.2f}%")
            col3.metric("市值", f"{info.get('marketCap', 0)/1e9:.2f} B")
            
            # 顯示股價圖
            hist = ticker.history(period="1mo")
            st.line_chart(hist['Close'])
            
            # 新聞顯示
            st.subheader("相關財經新聞")
            for item in ticker.news[:5]:
                st.markdown(f"- [{item.get('title')}]({item.get('link')})")
                
        except Exception as e:
            st.error(f"資料抓取失敗: {e}")
