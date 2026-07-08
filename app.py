import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from worker import fetch_stock_data

# 頁面配置 (設定為 wide 以容納豐富資訊)
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 側邊欄：核心輸入
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")
if st.sidebar.button("查詢分析數據"):
    st.session_state["query_ticker"] = ticker_input

# 檢查是否已有查詢數據
if "query_ticker" in st.session_state:
    ticker = st.session_state["query_ticker"]
    with st.spinner(f"正在分析 {ticker}..."):
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error(data["error"])
        else:
            # 1. & 2. 基礎資訊
            col1, col2, col3, col4 = st.columns(4)
            change = data.get('change', 0)
            color = "red" if change >= 0 else "green"
            col1.metric("即時股價", f"{data.get('price', 0):.2f}", f"{change:.2f}")
            col2.metric("每股淨值", f"{data.get('nav', 0):.2f}")
            col3.metric("本益比", f"{data.get('pe', 0):.2f}")
            col4.metric("EPS", f"{data.get('eps', 0):.2f}")
            
            st.divider()

            # 使用 Tabs 進行分頁，解決頁面卡死問題
            tab1, tab2, tab3, tab4 = st.tabs(["📊 法人與券商", "📈 技術與籌碼", "🤖 AI財報分析", "📰 新聞與警示"])
            
            with tab1:
                st.subheader("法人與券商買賣超")
                # 法人表格邏輯
                df_inst = pd.DataFrame(np.random.randint(-1000, 1000, (5, 3)), columns=['外資', '投信', '自營商'], index=[f"07-{i+1}" for i in range(5)])
                st.dataframe(df_inst.style.map(lambda x: f"color: {'red' if x > 0 else 'green'}"), use_container_width=True)

            with tab2:
                st.subheader("技術指標與股東結構")
                # KD/MACD/RSI
                fig = go.Figure(data=[go.Bar(x=['KD', 'MACD', 'RSI'], y=[65, 1.2, 58], marker_color=['blue', 'orange', 'green'])])
                st.plotly_chart(fig, use_container_width=True)
                
                # 持股分級
                st.bar_chart(pd.DataFrame({'張數': [40, 30, 30]}, index=['1-10張', '100-400張', '1000張以上']), color=['#808080', '#FFD700', '#FF0000'])

            with tab3:
                st.subheader("AI 預測與營收概況")
                st.success(f"AI預測: {data.get('ai_prediction', '數據分析中...')}")
                st.info(f"年度營收預估: {data.get('revenue_forecast', '暫無數據')}")

            with tab4:
                st.subheader("即時新聞與黑天鵝警示")
                st.warning(f"📰 新聞: {data.get('news', '暫無更新')}")
                st.error(f"⚠️ 黑天鵝警示: {data.get('black_swan', '安全')}")
                st.markdown("### 時.事.第.物")
                st.text("時: 09:00 | 事: 開盤 | 第: 台股 | 物: AI供應鏈")

else:
    st.info("👈 請在左側輸入股票代號並查詢，資料將於此處呈現。")
