import streamlit as st
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 使用絕對路徑
BASE_DIR = os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    return {}

all_data = load_data()

# 側邊欄：顯示除錯訊息
st.sidebar.write("系統狀態:", "正常" if not all_data.get("error") else "讀取錯誤")
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    # 如果讀取失敗，直接跳過資料層，改顯示系統訊息
    if "error" in all_data:
        st.error(f"無法讀取數據檔案: {all_data['error']}")
    elif ticker not in all_data:
        st.warning(f"找不到 {ticker}，請確認 Actions 是否已更新 market_data.json")
    else:
        data = all_data[ticker]
        st.success(f"成功載入 {ticker}")
        st.metric("即時股價", f"{data.get('price', 0):.2f}")
