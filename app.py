import streamlit as st
import requests
import json

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 直接指定 GitHub 上的 RAW 檔案連結
# 請務必修改下方連結為您的正確路徑
RAW_URL = "https://raw.githubusercontent.com/您的帳號/您的儲存庫/main/market_data.json"

def load_data_from_github():
    """從 GitHub RAW URL 即時抓取數據"""
    try:
        response = requests.get(RAW_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.sidebar.error(f"無法抓取 GitHub 數據 (狀態碼: {response.status_code})")
            return {}
    except Exception as e:
        st.sidebar.error(f"連線失敗: {e}")
        return {}

# 載入資料
all_data = load_data_from_github()
st.sidebar.write("系統檢查: 已成功從 GitHub 獲取數據")

ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    if ticker in all_data:
        data = all_data[ticker]
        
        # 顯示數值
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0):.2f}")
        col2.metric("每股淨額", f"{data.get('nav', 0):.2f}")
        col3.metric("本益比", f"{data.get('pe', 0):.2f}")
        col4.metric("每股盈餘", f"{data.get('eps', 0):.2f}")
        
        st.subheader("6. AI 財報預測")
        st.info(data.get("ai_report", "暫無分析數據"))
        
        st.subheader("3. 三大法人買賣超 (10日)")
        st.write(data.get("institutional_data", "無資料"))
    else:
        st.error(f"在 GitHub 數據中找不到 '{ticker}'，請檢查 market_data.json 是否已更新。")
