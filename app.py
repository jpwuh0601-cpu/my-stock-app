import streamlit as st
import pandas as pd
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取資料..."):
        data = fetch_stock_data(ticker)
        if data.get("error"):
            st.error(f"系統狀態: {data['error']}")
        else:
            info = data.get("info", {})
            st.subheader("2. 財務基本面指標")
            c1, c2, c3 = st.columns(3)
            c1.metric("股價", f"{info.get('currentPrice', 0):.2f}")
            c2.metric("EPS", f"{data.get('eps', 0):.2f}")
            
            # 安全讀取新聞
            st.subheader("8. 即時財經新聞")
            news = info.get("news", [])
            if isinstance(news, list):
                for n in news:
                    if isinstance(n, dict) and 'title' in n:
                        st.write(f"- {n['title']}")
                    else:
                        continue
            else:
                st.write("目前無最新新聞。")
