import streamlit as st
import json
import os
import pandas as pd
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式 (增強版，加入更多日誌與錯誤捕獲)
def load_data():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    logging.info(f"嘗試讀取數據檔案: {json_path}")
    
    if not os.path.exists(json_path):
        logging.error("找不到 market_data.json 檔案！")
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info("數據成功載入。")
            return data
    except Exception as e:
        logging.error(f"解析 JSON 檔案失敗: {e}")
        return None

# 初始化資料
data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    # 檢查是否有資料
    if data:
        # 1. 即時股價與指標
        col1, col2, col3, col4 = st.columns(4)
        
        price = str(data.get("price", "N/A"))
        bvps = str(data.get("bvps", "N/A"))
        
        col1.metric("即時股價", price)
        col2.metric("每股淨值", bvps)
        
        # 處理財報資料
        financials = data.get("financials", {})
        latest_quarter = list(financials.keys())[-1] if isinstance(financials, dict) and financials else None
        eps = str(financials.get(latest_quarter, {}).get("EPS", "N/A")) if latest_quarter else "N/A"
        
        col3.metric("最新 EPS", eps)
        col4.metric("本益比", str(data.get("pe_ratio", "N/A")))

        # 呈現其餘資料
        st.subheader("今年與去年每季財報")
        if isinstance(financials, dict) and financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)
        
        # ... (其餘內容保持不變)
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)
        else:
            st.write("暫無法人數據")
    else:
        st.error("無法讀取數據，請確認 market_data.json 是否已存在於倉庫根目錄。")
else:
    st.info("請輸入代碼後按下搜尋。")
