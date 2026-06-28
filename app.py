import streamlit as st
import json
import os

st.set_page_config(page_title="AI 投資決策儀表板", layout="wide")

st.sidebar.title("📈 決策復盤日記")

# 讀取歷史紀錄
if os.path.exists("journal.json"):
    with open("journal.json", "r", encoding="utf-8") as f:
        history = json.load(f)
        
    st.sidebar.subheader("歷史分析紀錄")
    for entry in reversed(history[-7:]): # 顯示最近 7 筆
        if st.sidebar.button(f"{entry['date']} 分析報告"):
            st.write(f"### {entry['date']} 復盤")
            st.info(entry['analysis'])
else:
    st.sidebar.info("尚未產生日記紀錄。")

st.title("AI 投資決策儀表板")
st.write("這是您的 AI 投資戰情室。請透過左側查看每日復盤紀錄。")
