import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面標題與佈局
st.set_page_config(page_title="AI 決策中樞", layout="wide")

# 快取數據抓取函數，解決 "Too Many Requests" 問題
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1mo")
    news = ticker.news
    return data, news

# 強制定義導航選單
st.sidebar.title("AI 決策中樞")
page = st.sidebar.radio("功能導航", ["Daily Stock Analysis", "投資復盤日記", "自動新聞讀取"])

# --- Daily Stock Analysis 頁面 ---
if page == "Daily Stock Analysis":
    st.title("Daily Stock Analysis")
    ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
    
    if st.button("抓取最新數據與新聞"):
        try:
            with st.spinner("資料抓取中..."):
                data, news = fetch_stock_data(ticker_input)
                
                if not data.empty:
                    st.line_chart(data['Close'])
                    st.success("數據抓取成功！")
                else:
                    st.warning("查無資料，請確認代號是否正確。")
                    
                if news:
                    st.subheader("相關財經新聞")
                    for n in news[:3]:
                        st.write(f"- [{n.get('title')}]({n.get('link')})")
        except Exception as e:
            st.error(f"資料抓取失敗: {e}")

# --- 投資復盤日記頁面 ---
elif page == "投資復盤日記":
    st.title("投資復盤日記")
    st.write("這裡是您的日記紀錄區。")
    diary_text = st.text_area("今日投資心得")
    if st.button("儲存紀錄"):
        st.success("日記已儲存！")

# --- 自動新聞讀取頁面 ---
else:
    st.title("自動新聞讀取")
    st.write("新聞系統運作中...")
