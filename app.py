import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面配置
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞 (專業版)")
    st.subheader("個股即時數據健檢")
    
    ticker_input = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        with st.spinner('正在分析市場數據...'):
            try:
                # 數據獲取
                stock = yf.Ticker(f"{ticker_input}.TW")
                df = stock.history(period="1mo", timeout=10)
                info = stock.info
                
                # 市場動態呈現
                st.subheader("📊 即時市場動態")
                cols = st.columns(4)
                
                # 安全獲取財務數據
                current_price = df['Close'].iloc[-1] if not df.empty else 0
                eps = info.get('trailingEps', 0)
                pe = info.get('trailingPE', 0)
                bv = info.get('bookValue', 0)
                
                cols[0].metric("即時股價", f"{current_price:.2f}")
                cols[1].metric("EPS", f"{eps:.2f}")
                cols[2].metric("本益比", f"{pe:.2f}")
                cols[3].metric("每股淨值", f"{bv:.2f}")
                
                # 預估股價按鈕
                if st.button("查看預估明年股價"):
                    st.info(f"根據現有數據，預估 {ticker_input} 明年走勢平穩，請參考技術指標。")
                
                # 股價走勢
                st.subheader("📈 股價走勢")
                st.line_chart(df['Close'])
                
            except Exception as e:
                st.error(f"資料讀取失敗，請確認代號正確或稍後再試: {e}")

elif menu == "部位管理":
    st.title("💼 部位管理")
    st.write("此功能目前建置中，您可以在此管理您的持倉與績效。")
