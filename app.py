import streamlit as st
import json
import os

# 設定頁面標題
st.set_page_config(page_title="個股分析儀表板", layout="wide")

st.title("📈 個股籌碼分析系統")

# --- 側邊欄：設定監控股票 ---
st.sidebar.subheader("⚙️ 設定監控股票")
with st.sidebar.form("ticker_form"):
    # 預設載入目前設定的股票
    current_ticker = "2330.TW"
    if os.path.exists("user_config.json"):
        with open("user_config.json", "r") as f:
            try:
                current_ticker = json.load(f).get("ticker", "2330.TW")
            except:
                pass
                
    user_ticker = st.text_input("輸入股票代號 (例如: 2330.TW)", value=current_ticker)
    submitted = st.form_submit_button("儲存並更新")

if submitted:
    # 儲存代號到設定檔
    with open("user_config.json", "w") as f:
        json.dump({"ticker": user_ticker}, f)
    
    # 這裡會將設定檔寫入，當您 Push 到 GitHub 時，Action 會自動觸發
    st.success(f"已儲存 {user_ticker}。請執行 Git Push，系統將自動更新數據。")
    st.info("提示：若您使用 GitHub 自動化，請確認已提交此設定檔案。")

# --- 顯示數據 ---
st.subheader("分析結果")
if os.path.exists("market_data.json"):
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        st.json(data)
else:
    st.warning("尚未有數據，請等待 GitHub Actions 執行分析。")
