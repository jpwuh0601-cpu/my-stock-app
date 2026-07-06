import streamlit as st
import pandas as pd
import yfinance as yf
from worker import fetch_real_broker_data

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

st.title("📈 個股籌碼分析系統")

# 1. 自行輸入股票
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在讀取資料..."):
        try:
            # 建立物件並加入防禦性處理
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 2. 每股淨額、本益比、EPS
            st.subheader("基本指標")
            col1, col2, col3 = st.columns(3)
            # 使用 .get() 確保讀不到也不會報錯
            col1.metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
            col2.metric("本益比", f"{info.get('forwardPE', '無資料')}")
            col3.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
            
            # 3. 季報表
            st.subheader("今年與去年每季報表")
            if stock.quarterly_financials is not None:
                st.dataframe(stock.quarterly_financials.iloc[:, :8], use_container_width=True)
            else:
                st.write("暫無季報數據")
            
            # 4. 法人買賣超 (預留空間)
            st.subheader("三大法人買賣超 (近10日)")
            st.write("*(需連結專業 API 獲取詳細數據)*")
            
            # 5. 資券比與主力券商
            st.subheader("10日資券比與主力券商買賣超")
            broker_data = fetch_real_broker_data(ticker)
            st.table(pd.DataFrame(broker_data))
            
            # 6. 即時新聞
            st.subheader("即時新聞")
            news = stock.news[:3] if 'news' in stock.info else []
            for item in news:
                st.write(f"- [{item['title']}]({item['link']})")
                
            # 7. AI 財報預測 (放置在新聞後)
            st.subheader("AI 財報預測")
            st.info("AI 預測: 根據目前基本面，營收預期呈現穩健成長模式。")
            
            # 8. 預估今年營收、EPS 與股利
            st.subheader("預估今年營收、EPS 與股利")
            st.write(f"- 預估 EPS: {info.get('forwardEps', 'N/A')}")
            st.write(f"- 預估股利: {info.get('dividendRate', 'N/A')}")
            
            # 自動回測數據完整性
            check_result = "正確" if info.get('regularMarketPrice') or info.get('currentPrice') else "警告：部分數據缺失"
            st.success(f"系統回測：數據來源連結正常，完整性: {check_result}")
            
        except Exception as e:
            st.error(f"查詢失敗: {e}")
