import streamlit as st
import requests
from worker import fetch_stock_data

# 設定
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# GitHub RAW URL
RAW_URL = "https://raw.githubusercontent.com/jpwuh0601-cpu/my-stock-app/main/market_data.json"

@st.cache_data(ttl=300)
def load_json_data():
    try:
        response = requests.get(RAW_URL, timeout=5)
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

# 載入靜態數據
all_data = load_json_data()

ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    # 邏輯：優先從 JSON 找，找不到則直接呼叫 worker 即時抓取
    if ticker in all_data:
        st.write("🔄 讀取靜態分析資料...")
        data = all_data[ticker]
        st.metric("即時股價", f"{data.get('price', 0):.2f}")
        st.info(data.get("ai_prediction", "無 AI 分析數據"))
    else:
        st.write("🔍 JSON 查無資料，嘗試即時網路連線抓取...")
        with st.spinner("正在從 Yahoo Finance 抓取最新股價..."):
            realtime_data = fetch_stock_data(ticker)
            if "error" in realtime_data:
                st.error(f"抓取失敗: {realtime_data['error']}，請確認代號是否正確。")
            else:
                st.metric("即時股價", f"{realtime_data.get('price', 0):.2f}")
                st.caption("註：此資料為即時網路抓取，非每日分析數據。")
