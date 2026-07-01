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
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    # 如果資料是空的字典，也要顯示提示
    if not data:
        st.error("目前找不到 market_data.json 檔案，請確認 GitHub Actions 是否已成功更新資料。")
    else:
        # 使用 dict.get(key, default) 確保永遠有值
        price = str(data.get("price", "-"))
        bvps = str(data.get("bvps", "-"))
        est_eps = str(data.get("est_eps", "-"))
        est_rev = str(data.get("est_revenue", "-"))
        margin = str(data.get("margin_ratio", "0"))

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", price)
        col2.metric("每股淨值", bvps)
        col3.metric("預估今年 EPS", est_eps)
        col4.metric("預估今年營收", est_rev)

        st.subheader("今年與去年每季財報")
        financials = data.get("financials", {})
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)

        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)

        st.subheader("10日資券比")
        st.metric("當前資券比", f"{margin}%")
        
        st.subheader("即時新聞")
        for news in data.get("news", ["暫無最新新聞"]):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "AI 分析中..."))
else:
    st.info("請輸入代碼並按下搜尋。")
