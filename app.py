import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式：確保絕對路徑讀取
def load_data():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# 載入資料
data = load_data()

# 側邊欄搜尋
st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    # 檢查是否讀取到資料
    if not data:
        st.error("目前找不到 market_data.json 檔案，請確認 GitHub Actions 是否已成功推送資料。")
    else:
        # 顯示關鍵數據區塊
        # 使用 str() 強制轉型，確保 st.metric 永遠有值
        price = str(data.get("price", "-"))
        bvps = str(data.get("bvps", "-"))
        est_eps = str(data.get("est_eps", "-"))
        est_rev = str(data.get("est_revenue", "-"))

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", price)
        col2.metric("每股淨值", bvps)
        col3.metric("預估今年 EPS", est_eps)
        col4.metric("預估今年營收", est_rev)

        # 財報區塊
        st.subheader("今年與去年每季財報")
        financials = data.get("financials", {})
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)
        else:
            st.write("目前無財報數據")

        # 三大法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)
        else:
            st.write("目前無法人買賣數據")

        # 10日資券比
        st.subheader("10日資券比")
        margin = str(data.get("margin_ratio", "0"))
        st.metric("當前資券比", f"{margin}%")
        
        # 即時新聞
        st.subheader("即時新聞")
        news_items = data.get("news", ["暫無最新新聞"])
        for news in news_items:
            st.write(f"• {news}")
            
        # AI 財報預測
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "AI 模型分析中..."))

else:
    st.info("請輸入代碼並按下搜尋按鈕。")
