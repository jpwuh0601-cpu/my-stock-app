import streamlit as st
import requests

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# GitHub RAW URL
RAW_URL = "https://raw.githubusercontent.com/jpwuh0601-cpu/my-stock-app/main/market_data.json"

@st.cache_data(ttl=3600)
def load_json_data():
    """強制讀取 GitHub JSON，移除即時抓取以避免 Rate Limit"""
    try:
        response = requests.get(RAW_URL, timeout=10)
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

# 載入數據
all_data = load_json_data()

# 顯示所有可用股票，方便使用者選擇
available_tickers = list(all_data.keys())
ticker = st.sidebar.selectbox("請選擇已分析的股票", options=available_tickers if available_tickers else ["無數據"])

if st.sidebar.button("查詢分析數據"):
    if ticker in all_data:
        data = all_data[ticker]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0):.2f}")
        col2.metric("每股淨額", f"{data.get('nav', 0):.2f}")
        col3.metric("本益比", f"{data.get('pe', 0):.2f}")
        col4.metric("每股盈餘", f"{data.get('eps', 0):.2f}")
        
        st.subheader("6. AI 財報預測")
        st.info(data.get("ai_prediction", "暫無 AI 分析數據"))
    else:
        st.error("查無資料。請確認 GitHub Actions 是否已成功更新 market_data.json。")
