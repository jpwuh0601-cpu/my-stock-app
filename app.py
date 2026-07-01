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
        except Exception as e:
            st.error(f"讀取資料錯誤: {e}")
            return None
    return None

data = load_data()

# 側邊欄搜尋
st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")
if st.sidebar.button("開始搜尋"):
    if data:
        # 顯示儀表板數據
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", f"{data.get('price', 0)}")
        col2.metric("每股淨值 (BVPS)", f"{data.get('bvps', 0)}")
        
        # 提取並顯示 EPS
        financials = data.get("financials", {})
        latest_quarter = list(financials.keys())[-1] if financials else "無數據"
        eps = financials.get(latest_quarter, {}).get("EPS", "N/A") if isinstance(financials.get(latest_quarter), dict) else "N/A"
        col3.metric(f"最新 EPS ({latest_quarter})", eps)
        
        col4.metric("本益比", f"{data.get('pe_ratio', 'N/A')}")

        st.subheader("今年與去年每季財報")
        if financials:
            df = pd.DataFrame.from_dict(financials, orient='index')
            # 修正 pandas 兼容性問題：使用 .map() 取代 .applymap()
            st.dataframe(df.style.map(lambda x: 'color: green' if isinstance(x, (int, float)) and x > 0 else 'color: red'))
        else:
            st.write("暫無財報數據")
    else:
        st.warning("請執行 GitHub Action 更新任務以取得數據。")

else:
    st.info("請在左側輸入股票代碼並按下搜尋。")
