import streamlit as st
import requests

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 直接使用 GitHub RAW URL 連結 (請確認此連結指向您 repo 中的 market_data.json)
RAW_URL = "https://raw.githubusercontent.com/jpwuh0601-cpu/my-stock-app/main/market_data.json"

@st.cache_data(ttl=600)
def load_data():
    try:
        response = requests.get(RAW_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception:
        return {}

# 載入資料
all_data = load_data()

ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    if not all_data:
        st.error("系統目前讀取不到數據，請確認 GitHub Actions 是否已成功推送檔案。")
    elif ticker in all_data:
        data = all_data[ticker]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0):.2f}")
        col2.metric("每股淨額", f"{data.get('nav', 0):.2f}")
        col3.metric("本益比", f"{data.get('pe', 0):.2f}")
        col4.metric("每股盈餘", f"{data.get('eps', 0):.2f}")
        
        st.subheader("6. AI 財報預測")
        st.info(data.get("ai_prediction", "數據載入中..."))
    else:
        st.warning(f"查無 '{ticker}' 的資料。")
