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

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 顯示儀表板數據
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0)}")
        col2.metric("每股淨值 (BVPS)", f"{data.get('bvps', 0)}")
        
        financials = data.get("financials", {})
        if isinstance(financials, dict) and financials:
            latest_quarter = list(financials.keys())[-1]
            eps = financials[latest_quarter].get("EPS", "N/A")
            col3.metric(f"最新 EPS ({latest_quarter})", eps)
        else:
            col3.metric("最新 EPS", "無數據")
            
        col4.metric("本益比", f"{data.get('pe_ratio', 'N/A')}")

        st.subheader("今年與去年每季財報")
        if isinstance(financials, dict) and financials:
            df = pd.DataFrame.from_dict(financials, orient='index')
            
            # 【關鍵修復】不要直接傳入 Styler 物件，改用 st.dataframe 顯示 DataFrame
            # 若要顏色效果，使用 column_config (Streamlit 較新的推薦做法)
            st.dataframe(df, use_container_width=True)
        else:
            st.write("暫無財報數據")
    else:
        st.warning("目前沒有數據，請檢查 GitHub Action 是否執行成功。")

else:
    st.info("請在左側輸入股票代碼並按下搜尋。")
