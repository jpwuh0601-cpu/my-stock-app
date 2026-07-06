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
            # 1. 取得物件與基礎數據
            stock = yf.Ticker(ticker)
            data = fetch_stock_data(ticker)
            
            # 2. 基本指標 (防禦處理)
            st.subheader("基本指標")
            col1, col2, col3 = st.columns(3)
            col1.metric("股價", data.get("price", "N/A"))
            col2.metric("每股淨值", stock.info.get('bookValue', "N/A"))
            col3.metric("EPS", data.get("eps", "N/A"))
            
            # 3. 季報表 (極致防禦處理，若無資料直接跳過，避免崩潰)
            st.subheader("近兩年每季財務概況")
            try:
                q_data = stock.quarterly_financials
                if q_data is not None and not q_data.empty:
                    st.dataframe(q_data.iloc[:, :4], use_container_width=True)
                else:
                    st.info("目前該個股無公開季報表數據。")
            except Exception:
                st.info("無法讀取季報表資料，可能是 Yahoo Finance 暫時無該個股資料。")
            
            # 4. 三大法人與資券比
            st.subheader("三大法人買賣超與資券比")
            broker_data = fetch_real_broker_data(ticker)
            st.table(pd.DataFrame(broker_data))
            
            # 5. 回測結果檢查
            if data.get("price") == 0:
                st.warning("⚠️ 警告：該代號在 Yahoo Finance 上查無資料或超時，請檢查代號是否正確。")
            else:
                st.success("✅ 資料來源檢查通過。")

        except Exception as e:
            st.error(f"系統發生例外錯誤: {str(e)}")
