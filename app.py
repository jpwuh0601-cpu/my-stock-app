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
    except Exception as e:
        st.error(f"JSON 讀取異常: {e}")
        return None

data = load_data()

st.sidebar.header("股票搜尋")
stock_code = st.sidebar.text_input("輸入台股代碼 (例如: 2330)")

if st.sidebar.button("開始搜尋"):
    if data:
        # 1. & 2. 關鍵數據區塊
        # 使用強制轉型確保 metric 函數永遠有值
        price = str(data.get("price", "N/A"))
        bvps = str(data.get("bvps", "N/A"))
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("即時股價", price)
        col2.metric("每股淨值", bvps)
        
        # 3. 財報預估區塊 (包含營收、EPS、股利)
        est_rev = str(data.get("est_revenue", "N/A"))
        est_eps = str(data.get("est_eps", "N/A"))
        col3.metric("預估今年 EPS", est_eps)
        col4.metric("預估今年營收", est_rev)

        # 4. 今年與去年每季報表
        st.subheader("今年與去年每季財報")
        financials = data.get("financials", {})
        if financials:
            st.dataframe(pd.DataFrame.from_dict(financials, orient='index'), use_container_width=True)
        else:
            st.write("目前無財報數據")

        # 5. 三大法人買賣超
        st.subheader("三大法人買賣超 (10日)")
        investors = data.get("institutional_investors", [])
        if investors:
            # 處理顏色：正數紅、負數綠
            df_inv = pd.DataFrame(investors)
            st.dataframe(df_inv.style.map(
                lambda val: 'color: red' if isinstance(val, (int, float)) and val > 0 
                else ('color: green' if isinstance(val, (int, float)) and val < 0 else ''), 
                subset=['買賣超']
            ), use_container_width=True)
        else:
            st.write("目前無法人買賣數據")

        # 6. 資券比
        st.subheader("10日資券比與主力券商")
        col_a, col_b = st.columns(2)
        col_a.metric("當前資券比", f"{data.get('margin_ratio', 0)}%")
        
        # 7. AI 財報預測與新聞 (依照您的排版要求)
        st.subheader("即時新聞")
        for news in data.get("news", ["暫無最新新聞"]):
            st.write(f"• {news}")
            
        st.subheader("AI 財報預測")
        st.info(data.get("ai_prediction", "AI 模型分析中，請稍候..."))
        
    else:
        st.error("無法讀取數據，請確認市場資料是否已同步。")
else:
    st.info("請輸入代碼後按下搜尋按鈕。")
