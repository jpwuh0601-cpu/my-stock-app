import streamlit as st
import json
import os

st.set_page_config(page_title="個股分析", layout="wide")

st.title("📈 個股籌碼分析系統")

# 1. 側邊欄：手動輸入代號
st.sidebar.subheader("⚙️ 設定")
with st.sidebar.form("ticker_input_form"):
    user_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
    submitted = st.form_submit_button("儲存代號")

if submitted:
    # 儲存代號
    with open("user_config.json", "w") as f:
        json.dump({"ticker": user_ticker}, f)
    st.sidebar.success(f"已儲存 {user_ticker}，請等待 GitHub Action 完成更新。")

# 2. 強制讀取數據區塊 (加入更詳盡的除錯)
st.subheader("分析結果")

if os.path.exists("market_data.json"):
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # 顯示所有內容，不依賴 Key，防止 Key 對不上導致顯示空白
        st.write("目前市場數據內容：")
        st.json(data)
        
    except Exception as e:
        st.error(f"JSON 解析失敗: {e}")
        st.write("檔案內容可能損毀，請檢查 GitHub 上的 market_data.json。")
else:
    st.warning("找不到 market_data.json，請確認 Action 是否已執行完成。")
