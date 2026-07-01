import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式
def load_data():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if not os.path.exists(json_path):
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# 強制將任何輸入轉為字串的函數
def to_str(val):
    if val is None:
        return "-"
    return str(val)

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 1. 關鍵數據區塊：直接在 metric 中處理，完全避免 None 的可能性
        col1, col2, col3, col4 = st.columns(4)
        
        # 這裡明確地傳入字串給 value 參數，絕對不會遺失
        col1.metric("即時股價", to_str(data.get("price")))
        col2.metric("每股淨值", to_str(data.get("bvps")))
        col3.metric("預估今年 EPS", to_str(data.get("est_eps")))
        col4.metric("預估今年營收", to_str(data.get("est_revenue")))

        # 2. 財報區塊
        st.subheader("今年與去年每季財報")
        financials = data.get("financials", {})
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)

        # 3. 法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)

        # 4. 資券比
        st.subheader("10日資券比")
        st.metric("當前資券比", to_str(data.get("margin_ratio")) + "%")
        
        # 5. 新聞與 AI 預測
        st.subheader("即時新聞")
        for news in data.get("news", ["暫無最新新聞"]):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "AI 分析中..."))
        
    else:
        st.error("無法載入資料，請確認 market_data.json 是否已存在。")
else:
    st.info("請輸入代碼後按下搜尋按鈕。")
