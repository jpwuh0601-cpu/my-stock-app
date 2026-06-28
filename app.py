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
            try: history = json.load(f)
            except: history = []
    
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
    ticker = st.text_input("輸入股票代號", "2330.TW")
    if st.button("抓取最新新聞"):
        try:
            time.sleep(1.5) # 增加冷卻時間
            t = yf.Ticker(ticker)
            news = t.news
            
            if not news:
                st.warning("目前暫無此股票的最新新聞，可能是 API 限制或無資料。")
            else:
                for n in news[:5]:
                    # 使用 .get() 避免 'title' 鍵值不存在時崩潰
                    title = n.get('title', '無標題')
                    link = n.get('link', '#')
                    st.write(f"**{title}**")
                    if st.button(f"解讀此則新聞", key=n.get('uuid', str(time.time()))):
                        analysis = f"AI 分析: 針對 {title}，建議密切觀察市場波動。"
                        st.info(analysis)
                        save_to_journal(ticker, analysis)
                        st.success("已存入復盤日記！")
        except Exception as e:
            # 顯示更具體的錯誤資訊以利診斷
            st.error(f"抓取新聞時遇到限制或錯誤，請稍候幾分鐘再試 (錯誤代碼: {str(e)})")

elif menu == "投資復盤日記":
    st.subheader("📖 歷史決策回顧")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                st.table(pd.DataFrame(data))
            except:
                st.write("紀錄檔格式錯誤。")
    else:
        st.write("尚無歷史紀錄。")
