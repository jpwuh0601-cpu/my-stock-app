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
    except:
        return None

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 1. & 2. 即時股價與每股淨值 (加強空值判斷)
        col1, col2, col3, col4 = st.columns(4)
        price = str(data.get("price", "N/A"))
        bvps = str(data.get("bvps", "N/A"))
        
        col1.metric("即時股價", price)
        col2.metric("每股淨值", bvps)
        
        # EPS 與本益比
        financials = data.get("financials", {})
        latest_quarter = list(financials.keys())[-1] if isinstance(financials, dict) and financials else "無數據"
        eps = str(financials.get(latest_quarter, {}).get("EPS", "N/A")) if latest_quarter != "無數據" else "N/A"
        
        col3.metric("最新 EPS", eps)
        col4.metric("本益比", str(data.get("pe_ratio", "N/A")))

        # 4. 財報表
        st.subheader("今年與去年每季財報")
        if isinstance(financials, dict) and financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)
        
        # 5. 三大法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if isinstance(investors, list) and len(investors) > 0:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)
        else:
            st.write("暫無法人數據")

        # 6. 資券比
        st.subheader("10日資券比")
        margin_ratio = str(data.get("margin_ratio", "N/A"))
        st.metric("當前資券比", f"{margin_ratio}%")

        # 7. 即時新聞與 AI 財報預測
        st.subheader("即時新聞")
        news_list = data.get("news", [])
        for news in news_list:
            st.write(f"- {news}")

        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "暫無預測資料"))

    else:
        st.warning("無法讀取數據，請檢查 market_data.json 是否已成功生成。")
else:
    st.info("請輸入代碼後按下搜尋。")
