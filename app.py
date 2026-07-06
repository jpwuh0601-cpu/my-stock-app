import streamlit as st
import pandas as pd
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

st.title("📈 個股籌碼分析系統")

ticker = st.sidebar.text_input("輸入股票代號", value="1301.TW")

if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在讀取資料..."):
        data = fetch_stock_data(ticker)
        info = data.get("info", {})

        # 1. 基本面
        st.subheader("2. 財務基本面指標")
        c1, c2, c3 = st.columns(3)
        c1.metric("股價", f"{info.get('currentPrice', 0):.2f}")
        c2.metric("EPS", f"{data.get('eps', 0):.2f}")
        c3.metric("本益比", f"{info.get('forwardPE', 0):.2f}")

        # 2. 法人數據
        st.subheader("4. 三大法人買賣超")
        try:
            inst_df = fetch_institutional_data(ticker)
            st.dataframe(inst_df.set_index("日期"), use_container_width=True)
        except:
            st.warning("法人數據讀取中...")

        # 3. 新聞區塊 (修正重點：加入 key 檢查)
        st.subheader("8. 即時財經新聞")
        news = info.get("news", [])
        if isinstance(news, list) and len(news) > 0:
            for n in news:
                # 確保只有當 title 存在且為字串時才顯示
                title = n.get("title")
                if title and isinstance(title, str):
                    st.write(f"- {title}")
        else:
            st.write("目前無最新財經新聞。")

        # 4. 狀態回報
        st.success("✅ 資料讀取完成")
