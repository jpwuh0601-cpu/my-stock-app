import streamlit as st
import json
import os

# 強制設定
st.set_page_config(page_title="股市儀表板", layout="wide")

st.title("📈 股市決策儀表板")

# 檢查資料
data_path = "market_data.json"
if not os.path.exists(data_path):
    st.error(f"找不到 {data_path}，請確認 GitHub Actions 是否已執行完成。")
else:
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 顯示列表
        tickers = list(data.keys())
        selected = st.selectbox("選擇股票", tickers)
        
        if selected:
            d = data[selected]
            st.metric("股價", d.get("price", "無資料"))
            st.write("詳細資料已載入")
    except Exception as e:
        st.error(f"資料讀取錯誤: {e}")
