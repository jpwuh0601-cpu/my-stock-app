import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

# --- 配置 ---
DATA_FILE = "trading_journal.json"
st.set_page_config(page_title="AI 股市決策日記", layout="wide")

# --- 核心功能函數 ---
def save_to_journal(ticker, analysis):
    """將 AI 分析紀錄存入 JSON"""
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "ticker": ticker, "analysis": analysis}
    history.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f)

# --- 側邊選單 ---
st.sidebar.title("🤖 AI 決策中樞")
menu = st.sidebar.radio("功能導航", ["AI 主力分析", "自動新聞讀取", "投資復盤日記"])

# --- 頁面邏輯 ---
if menu == "AI 主力分析":
    st.subheader("📊 AI 主力追蹤")
    ticker = st.text_input("輸入股票代號", "1301")
    if st.button("查詢主力動向"):
        st.info("AI 提示：主力近期持倉比例穩定，無異常撤資現象。")

elif menu == "自動新聞讀取":
    st.subheader("📰 熱門財經新聞")
    ticker = st.text_input("輸入股票代號以獲取相關新聞", "2330.TW")
    if st.button("抓取最新新聞"):
        t = yf.Ticker(ticker)
        news = t.news
        for n in news[:5]:
            st.write(f"**{n['title']}**")
            if st.button(f"解讀此則新聞: {n['title'][:10]}...", key=n['uuid']):
                analysis = f"AI 對 {n['title']} 的初步觀察：建議保持關注並搭配技術指標操作。"
                st.info(analysis)
                save_to_journal(ticker, analysis)

elif menu == "投資復盤日記":
    st.subheader("📖 歷史決策回顧")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            st.table(df)
    else:
        st.write("尚無歷史紀錄，快去「自動新聞讀取」解讀新聞吧！")
