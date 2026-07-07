import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 獲取當前工作目錄，確保路徑正確
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """讀取市場數據，增加除錯資訊"""
    if not os.path.exists(DATA_PATH):
        st.sidebar.error(f"找不到檔案: {DATA_PATH}")
        return {}
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            st.sidebar.error(f"JSON 格式錯誤: {e}")
            return {}

all_data = load_data()
st.sidebar.write("目前 JSON 內的股票:", list(all_data.keys()))

ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = all_data.get(ticker)
    
    if not data:
        st.error(f"查無 '{ticker}' 的資料。")
    else:
        # 對接正確的階層結構
        # 根據您的 JSON 截圖，資料在 stock_entry["raw_info"] 下
        raw = data.get("raw_info", data) # 如果沒有 raw_info 就讀取自己
        info = raw.get("info", {})
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{raw.get('price', 0):.2f}")
        col2.metric("每股淨額 (NAV)", f"{info.get('bookValue', 0):.2f}")
        col3.metric("本益比 (PE)", f"{info.get('trailingPE', 0):.2f}")
        col4.metric("每股盈餘 (EPS)", f"{raw.get('eps', 0):.2f}")
        
        st.subheader("6. AI 財報預測")
        st.info(data.get("ai_report", "暫無分析數據"))
