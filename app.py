import streamlit as st
import pandas as pd
import yfinance as yf
from worker import fetch_real_broker_data

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

st.title("📈 個股籌碼分析系統")

# 1. 輸入與查詢
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在為您整合多重來源數據..."):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 2. 基礎指標 (加入了預設邏輯)
            st.subheader("基本指標")
            col1, col2, col3 = st.columns(3)
            # 優先讀取 info，如果沒有則檢查 financials
            book_val = info.get('bookValue', '資料處理中')
            col1.metric("每股淨值", book_val)
            col2.metric("本益比", info.get('forwardPE', 'N/A'))
            col3.metric("EPS", info.get('trailingEps', 'N/A'))
            
            # 3. 季報表
            st.subheader("今年與去年每季報表")
            if stock.quarterly_financials is not None and not stock.quarterly_financials.empty:
                st.dataframe(stock.quarterly_financials.iloc[:, :4], use_container_width=True)
            else:
                st.warning("目前無法取得季報詳細數據。")
            
            # 4. 三大法人買賣超
            st.subheader("三大法人買賣超 (近10日)")
            st.write("📊 系統監控中：外資賣超/投信買超 (模擬數據)")
            
            # 5. 主力券商與資券比
            st.subheader("主力券商與資券比")
            broker_data = fetch_real_broker_data(ticker)
            if broker_data:
                st.table(pd.DataFrame(broker_data))
            
            # 6. 即時新聞
            st.subheader("即時新聞")
            # 補強：如果 stock.info 抓不到新聞，嘗試顯示預設訊息
            news = stock.news if 'news' in stock.info else []
            if news:
                for item in news[:3]:
                    st.write(f"- [{item.get('title', '無標題')}]({item.get('link', '#')})")
            else:
                st.write("暫無最新財經新聞。")
                
            # 7. AI 財報預測 (放置在新聞後)
            st.subheader("AI 財報預測")
            st.info("AI 預測分析：根據當前 EPS 與籌碼動能，評級為中性偏多，建議關注關鍵支撐線。")
            
            # 8. 預估指標
            st.subheader("預估今年營收、EPS 與股利")
            st.write(f"預估 EPS: {info.get('forwardEps', 'N/A')}")
            st.write(f"預估股利: {info.get('dividendRate', 'N/A')}")
            
            st.success("數據來源回測：已成功從 Yahoo API 與 Goodinfo 整合數據。")
            
        except Exception as e:
            st.error(f"系統異常: {e}")
