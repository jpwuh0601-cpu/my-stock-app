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

st.set_page_config(page_title="AI 股市決策日記", layout="wide")
st.sidebar.title("🤖 AI 決策中樞")
menu = st.sidebar.radio("功能導航", ["自動新聞讀取", "投資復盤日記"])

if menu == "自動新聞讀取":
    st.subheader("📰 熱門財經新聞")
    ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    if st.button("抓取最新新聞"):
        try:
            time.sleep(1) 
            t = yf.Ticker(ticker)
            news = t.news
            if not news:
                st.warning("暫無相關新聞。")
            else:
                for n in news[:5]:
                    st.write(f"**{n.get('title', '無標題')}**")
                    if st.button(f"解讀此則新聞", key=n.get('uuid', str(time.time()))):
                        analysis = f"AI 分析: 針對 {n.get('title')} 的市場趨勢觀察。"
                        st.info(analysis)
                        save_to_journal(ticker, analysis)
                        st.success("已存入復盤日記！")
        except Exception as e:
            st.error("市場數據請求冷卻中，請稍候幾分鐘後再試。")

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
