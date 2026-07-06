import streamlit as st
import pandas as pd
import yfinance as yf
from worker import fetch_stock_data, fetch_real_broker_data

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在為您處理數據..."):
        try:
            # 1. 取得物件
            stock = yf.Ticker(ticker)
            info = stock.info
            data = fetch_stock_data(ticker)
            
            # 2. 基本指標 (防禦處理)
            st.subheader("基本指標")
            col1, col2, col3 = st.columns(3)
            col1.metric("股價", data.get("price", "N/A"))
            col2.metric("每股淨值", info.get('bookValue', "N/A"))
            col3.metric("EPS", data.get("eps", "N/A"))
            
            # 3. 季報表 (修正 AttributeError: NoneType)
            st.subheader("近兩年每季財務概況")
            q_data = stock.quarterly_financials
            if q_data is not None and not q_data.empty:
                st.dataframe(q_data.iloc[:, :4], use_container_width=True)
            else:
                st.info("目前該個股無公開季報表詳細數據。")
            
            # 4. 三大法人與資券比
            st.subheader("三大法人買賣超與資券比")
            broker_data = fetch_real_broker_data(ticker)
            st.table(pd.DataFrame(broker_data))
            
            # 5. 回測結果檢查
            if data.get("price") == 0:
                st.error("⚠️ 資料回測失敗：無法從 Yahoo Finance 獲取有效股價。")
            else:
                st.success("✅ 資料來源檢查通過：系統已讀取成功。")

        except Exception as e:
            st.error(f"頁面渲染錯誤: {e}")
