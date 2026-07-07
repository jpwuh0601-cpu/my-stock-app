import streamlit as st
import requests

# 頁面設定
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 使用 GitHub RAW URL 連結 (請確認這是您的正確網址)
RAW_URL = "https://raw.githubusercontent.com/jpwuh0601-cpu/my-stock-app/refs/heads/main/market_data.json"

@st.cache_data(ttl=600)
def load_data():
    """使用 requests 抓取資料，避免過度依賴檔案系統"""
    try:
        response = requests.get(RAW_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception:
        return {}

# 不要在此處直接執行 load_data()，請在點擊按鈕時才執行以加速啟動
if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        all_data = load_data()
        ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
        data = all_data.get(ticker)
        
        if data:
            st.metric("即時股價", f"{data.get('price', 0):.2f}")
            st.info(data.get("ai_report", "分析中..."))
        else:
            st.error("查無資料，請確認 Actions 已順利更新 market_data.json")
