import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 強制獲取絕對路徑，確保讀取的是同一個檔案
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """讀取市場數據並顯示路徑偵錯"""
    st.sidebar.write(f"系統檢查: 檔案路徑 {FILE_PATH}")
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            st.sidebar.error(f"解析 JSON 失敗: {e}")
            return {}
    else:
        st.sidebar.error("找不到 market_data.json 檔案")
        return {}

all_data = load_data()
st.sidebar.write("目前 JSON 內的股票:", list(all_data.keys()))

ticker = st.sidebar.text_input("輸入股票代號 (如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    if ticker in all_data:
        data = all_data[ticker]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0):.2f}")
        col2.metric("每股淨額", f"{data.get('nav', 0):.2f}")
        col3.metric("本益比", f"{data.get('pe', 0):.2f}")
        col4.metric("每股盈餘", f"{data.get('eps', 0):.2f}")
        st.subheader("6. AI 財報預測")
        st.info(data.get("ai_report", "暫無分析數據"))
    else:
        st.error(f"找不到 {ticker}，請確認 market_data.json 內容。")
