import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式
def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

data = load_data()

# 搜尋邏輯
st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 顯示儀表板數據
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0)}")
        col2.metric("每股淨值 (BVPS)", f"{data.get('bvps', 0)}")
        
        # 修正 EPS 讀取邏輯以符合您提供的 JSON 結構
        financials = data.get("financials", {})
        # 因為 financials 結構為 {"2025Q1": {"EPS": 5.2, ...}}
        if financials:
            latest_quarter = list(financials.keys())[-1]
            eps = financials[latest_quarter].get("EPS", "N/A")
            col3.metric(f"最新 EPS ({latest_quarter})", eps)
        else:
            col3.metric("最新 EPS", "N/A")
            
        col4.metric("本益比", f"{data.get('pe_ratio', 'N/A')}")

        st.subheader("今年與去年每季財報")
        if financials:
            df = pd.DataFrame.from_dict(financials, orient='index')
            # 確保使用 .map 避免 pandas 3.0+ 錯誤
            st.dataframe(df.style.map(lambda x: 'color: green' if isinstance(x, (int, float)) and x > 0 else 'color: red'))
        else:
            st.write("暫無財報數據")
    else:
        st.warning("目前沒有數據，請確保 GitHub Action 已成功更新 market_data.json。")

else:
    st.info("請在左側輸入股票代碼並按下搜尋。")
