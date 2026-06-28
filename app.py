import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import time
from datetime import datetime

# 初始化紀錄檔案
DATA_FILE = "trading_journal.json"

def save_to_journal(ticker, analysis):
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
        "ticker": ticker, 
        "analysis": analysis
    })
    with open(DATA_FILE, "w") as f:
        json.dump(history, f)

@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    t = yf.Ticker(ticker)
    return t.history(period="1mo")

@st.cache_data(ttl=3600)
def get_news_cached(ticker):
    t = yf.Ticker(ticker)
    return t.news

# 應用程式設定
st.set_page_config(page_title="AI 股市決策日記", layout="wide")
st.sidebar.title("🤖 AI 決策中樞")

# 強制定義導航，確保 Daily Stock Analysis 永遠在側邊欄
menu = st.sidebar.radio("功能導航", ["Daily Stock Analysis", "投資復盤日記"])

if menu == "Daily Stock Analysis":
    st.subheader("📰 熱門財經新聞與走勢")
    ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if st.button("抓取最新數據與新聞"):
        try:
            with st.spinner('正在分析市場數據...'):
                data = get_stock_data(ticker)
                st.line_chart(data['Close'])
                
                news = get_news_cached(ticker)
                if not news:
                    st.warning("暫無相關新聞。")
                else:
                    for n in news[:5]:
                        st.write(f"**{n.get('title', '無標題')}**")
        except Exception as e:
            st.error(f"資料抓取失敗: {e}")

elif menu == "投資復盤日記":
    st.subheader("📖 歷史決策回顧")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                st.table(pd.DataFrame(data))
            except:
                st.write("讀取紀錄發生錯誤。")
    else:
        st.write("尚無歷史紀錄。")
