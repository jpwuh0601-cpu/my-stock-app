import streamlit as st
import json
import os

# 設定頁面
st.set_page_config(page_title="股市儀表板", layout="wide")

st.title("📈 股市儀表板")

# 強制尋找根目錄下的 JSON
json_path = os.path.join(os.getcwd(), "market_data.json")

if not os.path.exists(json_path):
    st.error(f"找不到數據檔案: {json_path}。請確認 GitHub Actions 已成功將 market_data.json 推送至根目錄。")
else:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        tickers = list(data.keys())
        selected = st.selectbox("選擇股票", tickers)
        
        if selected:
            d = data[selected]
            st.metric("股價", d.get("price", "無資料"))
            st.write("詳細資料已載入")
    except Exception as e:
        st.error(f"讀取錯誤: {e}")
