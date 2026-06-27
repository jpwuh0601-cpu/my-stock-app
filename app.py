import streamlit as st
import twstock
import pandas as pd
import random
import requests
from datetime import datetime

st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (自動化日誌版)")

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# 記錄每日健檢歷史的函數
def log_to_file(message):
    with open("daily_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {message}\n")

# 優化後的 LINE 推送 (Markdown 格式)
def send_line_message(token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)

# (其餘函數 fetch_data, ai_score, calculate_strategies 保持不變...)
# ... [上述函數維持原邏輯] ...

menu = st.sidebar.radio("核心模組", ["選股矩陣", "部位對帳單", "自動報告生成", "執行日誌"])
token = st.secrets.get("LINE_NOTIFY_TOKEN")

# ... [選股矩陣與部位對帳單區塊保持原邏輯] ...

elif menu == "自動報告生成":
    st.info("系統將整理部位健檢結果並推送至 LINE。")
    if st.button("觸發每日健檢報告"):
        report = "📊 *AI 每日持股健檢報告*\n"
        for item in st.session_state.portfolio:
            score = ai_score(random.random(), random.random(), 2, random.randint(0,10)) # 簡化測試
            status = "✅ 良好" if score >= 30 else "⚠️ 建議檢視"
            report += f"- {item['代號']}: 評分 {score} ({status})\n"
        
        send_line_message(token, report)
        log_to_file(report)
        st.success("健檢報告已推送並寫入日誌。")

elif menu == "執行日誌":
    st.subheader("歷史決策記錄")
    try:
        with open("daily_log.txt", "r", encoding="utf-8") as f:
            st.text(f.read())
    except:
        st.write("目前尚無記錄。")
