import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 【關鍵修復】取得 app.py 所在的資料夾路徑，強制確保讀取到正確的 JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "market_data.json")

def load_data():
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"檔案讀取失敗: {e}")
            return None
    else:
        st.error(f"找不到檔案: {json_path}") # 除錯用
        return None

data = load_data()

# 搜尋邏輯
st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
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
            st.dataframe(df, use_container_width=True)
        else:
            st.write("暫無財報數據")
    else:
        st.warning("目前沒有數據，請確保 market_data.json 已生成。")
else:
    st.info("請輸入代碼後按下搜尋。")
