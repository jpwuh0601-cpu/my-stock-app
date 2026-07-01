import streamlit as st
import json
import os
import pandas as pd

# 頁面設定
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 讀取數據函式 (加入除錯機制)
def load_data():
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if not os.path.exists(json_path):
        st.error(f"找不到檔案: {json_path}")
        return None
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON 格式錯誤: {e}")
        return None

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 1 & 2. 即時股價與每股淨值
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", str(data.get("price", "N/A")))
        col2.metric("每股淨值", str(data.get("bvps", "N/A")))
        
        # EPS 與本益比
        financials = data.get("financials", {})
        latest_quarter = list(financials.keys())[-1] if financials else "無數據"
        eps = financials.get(latest_quarter, {}).get("EPS", "N/A") if financials else "N/A"
        col3.metric("最新 EPS", str(eps))
        col4.metric("本益比", str(data.get("pe_ratio", "N/A")))

        # 4. 今年與去年每季報表
        st.subheader("今年與去年每季財報")
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)
        
        # 5. 三大法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            st.dataframe(pd.DataFrame(investors), use_container_width=True)
        else:
            st.write("暫無數據")

        # 6. 10日資券比
        st.subheader("10日資券比")
        st.metric("當前資券比", f"{data.get('margin_ratio', 'N/A')}%")

        # 7. 即時新聞與 AI 財報預測
        st.subheader("即時新聞")
        for news in data.get("news", ["暫無新聞"]):
            st.write(f"- {news}")

        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "暫無預測"))

    else:
        st.warning("數據讀取失敗，請檢查市場資料是否已更新。")
else:
    st.info("請輸入代碼後按下搜尋。")
