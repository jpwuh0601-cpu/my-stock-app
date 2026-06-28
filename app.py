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
    """將 AI 分析紀錄存入 JSON"""
    history = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
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
            time.sleep(1) # 增加冷卻防止報錯
            t = yf.Ticker(ticker)
            news = t.news
            
            if not news:
                st.warning("目前暫無此股票的最新新聞。")
            else:
                for n in news[:5]:
                    title = n.get('title', '無標題')
                    st.write(f"**{title}**")
                    if st.button(f"解讀此則新聞", key=n.get('uuid', str(time.time()))):
                        analysis = f"AI 分析: 針對 {title}，建議密切觀察市場波動。"
                        st.info(analysis)
                        save_to_journal(ticker, analysis)
                        st.success("已存入復盤日記！")
        except Exception as e:
            st.error(f"數據讀取受限，請稍候再試 (Error: {str(e)})")

elif menu == "投資復盤日記":
    st.subheader("📖 歷史決策回顧")
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                st.table(pd.DataFrame(data))
        except:
            st.write("紀錄檔讀取錯誤。")
    else:
        st.write("尚無歷史紀錄。")
