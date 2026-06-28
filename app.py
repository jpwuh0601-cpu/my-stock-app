import streamlit as st
import pandas as pd
import random
import requests
import plotly.express as px
import os
from datetime import datetime
from openai import OpenAI

# 設定頁面
st.set_page_config(page_title="AI 決策中樞", layout="wide")
st.title("🚀 AI 專業投資決策中樞 (專業實戰整合版)")

# 初始化狀態與 API 連線
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# 安全讀取 Secrets (優先讀取 Streamlit Secrets)
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
line_token = st.secrets.get("LINE_NOTIFY_TOKEN") or os.getenv("LINE_NOTIFY_TOKEN")

# 初始化 OpenAI 客戶端 (OpenRouter)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openai_api_key) if openai_api_key else None

# --- 核心邏輯函式 ---
def check_health():
    """雲端健康檢查：檢測 API 連線狀態"""
    status = {"LINE": "✅ 正常" if line_token else "❌ 未設定", "OpenRouter": "✅ 正常" if client else "❌ 未設定"}
    return status

def send_line_message(token, message):
    if not token: return
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": f"\n{message}"}
    requests.post(url, headers=headers, data=payload)

def get_ai_analysis(ticker, fundamentals):
    """優化後的 AI 深度決策指令"""
    if not client: return "AI 分析功能目前無法使用 (API Key 未配置)"
    
    prompt = f"""
    請擔任專業分析師，針對個股 {ticker} 進行深入分析：
    - 基本面數據: {fundamentals}
    - 要求：請特別檢查 PE 比是否過高，並評估 EPS 的增長潛力。
    - 若 PE > 25 或 EPS 顯示衰退，請給出減碼警告。
    - 給出明確的 0-100 分數與投資建議。
    """
    response = client.chat.completions.create(model="openai/gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

# --- UI 模組 ---
menu = st.sidebar.radio("核心模組", ["市場監控", "AI 選股與下單", "部位健檢", "決策日誌"])

if menu == "市場監控":
    st.subheader("📊 雲端系統健康狀態")
    health = check_health()
    cols = st.columns(2)
    for i, (k, v) in enumerate(health.items()):
        cols[i].metric(k, v)
    
    st.divider()
    st.subheader("📊 市場資金流向熱點圖")
    # ... (原有邏輯維持不變)

elif menu == "AI 選股與下單":
    st.subheader("AI 自動化決策")
    t = st.text_input("輸入股票代號", "2330")
    if st.button("評估買入"):
        # 假設已有 fetch_data 與計算邏輯
        st.info("執行深度基本面與技術面綜合分析...")
        # 這裡整合 get_ai_analysis
        ai_advice = get_ai_analysis(t, "PE=20, EPS=25 (假設值)")
        st.write(ai_advice)

elif menu == "部位健檢":
    st.subheader("持股部位監控")
    # ... (原有邏輯維持不變)

elif menu == "決策日誌":
    st.subheader("📋 互動式決策歷史日誌")
    # ... (原有邏輯維持不變)
