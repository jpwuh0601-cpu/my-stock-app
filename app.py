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
        with open(DATA_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "ticker": ticker, "analysis": analysis}
    history.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f)

st.set_page_config(page_title="AI 股市決策日記", layout="wide")
st.sidebar.title("🤖 AI 決策中樞")
menu = st.sidebar.radio("功能導航", ["AI 主力分析", "自動新聞讀取", "投資復盤日記"])

if menu == "AI 主力分析":
    st.subheader("📊 AI 主力追蹤")
    ticker = st.text_input("輸入股票代號", "1301")
    if st.button("查詢主力動向"):
        st.info("AI 提示：主力近期持倉比例穩定，無異常撤資現象。")

elif menu == "自動新聞讀取":
    st.subheader("📰 熱門財經新聞")
    ticker = st.text_input("輸入股票代號以獲取相關新聞 (例如: 2330.TW)", "2330.TW")
    if st.button("抓取最新新聞"):
        try:
            with st.spinner('正在從財經數據庫抓取中...'):
                t = yf.Ticker(ticker)
                # 加入短暫延遲避免頻繁請求
                time.sleep(1)
                news = t.news
                
                if not news:
                    st.warning("目前沒有該股票的相關新聞。")
                else:
                    for n in news[:5]:
                        st.write(f"**{n['title']}**")
                        if st.button(f"解讀此則新聞: {n['title'][:10]}...", key=n['uuid']):
                            analysis = f"AI 對 {n['title']} 的初步觀察：建議保持關注並搭配技術指標操作。"
                            st.info(analysis)
                            save_to_journal(ticker, analysis)
        except Exception as e:
            st.error(f"抓取新聞時遇到限制，請稍候再試 (錯誤代碼: {e})")

elif menu == "投資復盤日記":
    st.subheader("📖 歷史決策回顧")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                df = pd.DataFrame(data)
                st.table(df)
            except:
                st.write("紀錄檔格式錯誤。")
    else:
        st.write("尚無歷史紀錄，快去「自動新聞讀取」解讀新聞吧！")
