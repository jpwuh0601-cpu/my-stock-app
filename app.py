import streamlit as st
import json
import os

st.set_page_config(page_title="個股分析", layout="centered")

st.title("📈 個股分析儀表板")

# 側邊欄：手動輸入代號
st.sidebar.subheader("⚙️ 設定")
with st.sidebar.form("ticker_input_form"):
    user_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
    submitted = st.form_submit_button("儲存代號")

if submitted:
    with open("user_config.json", "w") as f:
        json.dump({"ticker": user_ticker}, f)
    st.sidebar.success(f"已儲存 {user_ticker}，請等待後台更新。")

# 顯示分析資料
st.subheader("分析結果")
if os.path.exists("market_data.json"):
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # 強制只顯示該代號的內容
            ticker = list(data.keys())[0]
            st.write(f"### 目前分析標的: {ticker}")
            st.json(data[ticker])
    except Exception as e:
        st.error(f"讀取資料發生錯誤: {e}")
else:
    st.info("尚無資料，請確認後台分析是否已完成。")
