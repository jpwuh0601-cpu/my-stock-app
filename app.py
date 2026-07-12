import streamlit as st
import json
import os

# 1. 強制設定配置
st.set_page_config(page_title="股市儀表板", layout="wide")

st.title("📈 股市決策儀表板")

# 2. 加入除錯顯示，確保我們知道程式是否有跑起來
st.write("系統檢查：正在讀取資料...")

# 3. 確保檔案讀取不會中斷主執行緒
data = {}
if os.path.exists("market_data.json"):
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        st.error(f"檔案解析失敗: {e}")
else:
    st.warning("找不到 market_data.json，請檢查 GitHub Actions 是否成功產生檔案。")

# 4. 只有在資料存在時才執行渲染
if data:
    tickers = list(data.keys())
    selected = st.selectbox("請選擇股票", tickers)
    
    if selected:
        d = data[selected]
        # 使用簡單的顯示，避免複雜元件崩潰
        st.write(f"代號: {selected}")
        st.metric("股價", d.get("price", "無資料"))
else:
    st.info("尚未載入資料，請確認環境設定。")
