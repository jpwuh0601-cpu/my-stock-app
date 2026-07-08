import streamlit as st
import pandas as pd
import numpy as np

# 頁面配置 (必須在最上方)
st.set_page_config(page_title="股市儀表板", layout="wide")

st.title("📈 專業股市決策儀表板")

# 模擬數據生成函數
def get_mock_data(ticker):
    # 這裡未來可改為 worker.fetch_stock_data(ticker)
    return {
        "price": 100.0,
        "change": 2.5,
        "nav": 50.0,
        "pe": 15.0,
        "eps": 5.0
    }

# 側邊欄與主要輸入
ticker = st.sidebar.text_input("輸入股票代號", "2330")

if st.sidebar.button("查詢分析"):
    with st.spinner("載入資料中..."):
        data = get_mock_data(ticker)
        
        # 1. 即時股價 (紅漲綠跌)
        st.subheader(f"即時數據: {ticker}")
        color = "red" if data['change'] >= 0 else "green"
        st.markdown(f"### 股價: {data['price']} | 漲跌: :{color}[{data['change']}]")
        
        # 2. 基本面資訊
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨額", data['nav'])
        c2.metric("本益比", data['pe'])
        c3.metric("EPS", data['eps'])

        # 3. 法人籌碼 (簡化版，避免過大記憶體消耗)
        st.markdown("### 三大法人買賣超")
        df = pd.DataFrame(np.random.randint(-100, 100, (5, 3)), columns=["外資", "投信", "自營商"])
        st.dataframe(df.style.map(lambda x: 'color: red' if x > 0 else 'color: green'))

        st.success("數據載入完成。")
else:
    st.info("請在左側輸入代號並點擊查詢。")
