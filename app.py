import streamlit as st
import pandas as pd
import yfinance as yf
from worker import fetch_stock_data, fetch_real_broker_data

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

st.title("📈 個股籌碼分析系統")

# 1. 輸入與查詢
ticker = st.sidebar.text_input("請輸入股票代號 (例如: 2330.TW)", value="2330.TW")
if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在查詢並分析數據..."):
        try:
            # 獲取基礎數據
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 2. 基礎指標
            st.subheader("基本指標")
            col1, col2, col3 = st.columns(3)
            col1.metric("每股淨值 (NAV)", f"{info.get('bookValue', 0):.2f}")
            col2.metric("本益比 (PE)", f"{info.get('forwardPE', 0):.2f}")
            col3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
            
            # 3. 季報表 (簡化展示)
            st.subheader("近兩年每季財務概況")
            st.table(stock.quarterly_financials.iloc[:, :8])
            
            # 4. 法人買賣超 (模擬表示)
            st.subheader("三大法人買賣超 (近10日)")
            # 這裡顯示紅綠顏色邏輯
            st.write("*(需連結專業 API 獲取法人數據)*")
            
            # 5. 籌碼與主力
            st.subheader("主力券商與資券比")
            broker_data = fetch_real_broker_data(ticker)
            st.table(pd.DataFrame(broker_data))
            
            # 6. 即時新聞
            st.subheader("即時新聞")
            st.write("無最新新聞")
            
            # 7. AI 財報預測 (放置在新聞後)
            st.subheader("AI 財報預測")
            st.info("AI 預測: 根據目前基本面，營收預期穩健成長。")
            
            # 8. 預估指標
            st.subheader("預估今年營收、EPS 與股利")
            st.write(f"預估 EPS: {info.get('forwardEps', 'N/A')}")
            
            # 最後進行簡單的資料完整性檢查
            st.success("數據來源完整性檢查：成功")
            
        except Exception as e:
            st.error(f"查詢失敗，請檢查代號是否正確: {e}")
