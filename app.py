import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式 (修正絕對路徑問題)
def load_data():
    # 使用當前腳本目錄確保路徑正確
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if not os.path.exists(json_path):
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# 安全數值獲取函式 (保證不回傳 None)
def safe_metric(label, data, key):
    val = data.get(key)
    # 如果 val 是 None，強制顯示 '-'，避免 st.metric 報錯
    display_val = str(val) if val is not None else "-"
    st.metric(label, display_val)

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 1. 關鍵數據區塊 (使用 safe_metric 確保不會報錯)
        col1, col2, col3, col4 = st.columns(4)
        with col1: safe_metric("即時股價", data, "price")
        with col2: safe_metric("每股淨值", data, "bvps")
        with col3: safe_metric("預估今年 EPS", data, "est_eps")
        with col4: safe_metric("預估今年營收", data, "est_revenue")

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
        st.metric("當前資券比", f"{data.get('margin_ratio', 0)}%")
        
        # 5. 新聞與 AI 預測
        st.subheader("即時新聞")
        for news in data.get("news", ["暫無最新新聞"]):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "AI 分析中..."))
        
    else:
        st.error("無法載入資料，請確認市場資料是否已更新 (market_data.json)。")
else:
    st.info("請輸入代碼並按下搜尋。")
