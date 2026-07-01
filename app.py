import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")
st.title("📊 AI 智能投資決策儀表板")

# 修正：強制指定絕對路徑，確保與 GitHub Actions 推送位置一致
# /mount/src/my-stock-app/ 是 Streamlit Cloud 的標準根目錄
FILE_PATH = "/mount/src/my-stock-app/market_data.json"

def load_data():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return None
    return None

data = load_data()

if data is None:
    st.error(f"❌ 無法讀取資料檔，請確認檔案是否存在於: {FILE_PATH}")
    st.write("當前目錄所有檔案:", os.listdir('/mount/src/my-stock-app/'))
else:
    # 顯示核心數據
    price = str(data.get("price", "-"))
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("即時股價", price)
    col2.metric("每股淨值", data.get("bvps", "-"))
    col3.metric("預估營收", data.get("est_revenue", "-"))
    col4.metric("預估 EPS", data.get("est_eps", "-"))
    col5.metric("預估股利", data.get("est_dividend", "-"))
    col6.metric("10日資券比", f"{data.get('margin_ratio', 0)}%")
    
    # ... 其餘 UI 邏輯與之前相同
    st.success("✅ 資料載入成功")
