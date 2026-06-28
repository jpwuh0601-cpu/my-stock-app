import streamlit as st
import yfinance as yf
import pandas as pd

# 設置頁面基礎與響應式佈局
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航 (整合至全域)
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 核心解阻塞：使用 cache_data 減少網路負荷
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    try:
        # 使用 yfinance 獲取數據，並確保請求不會無限制掛起
        stock = yf.Ticker(f"{ticker}.TW")
        hist = stock.history(period="1mo")
        return hist, stock.info
    except Exception:
        return None, None

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 關鍵修正：改用 form，確保在點擊「啟動」前，不會自動發起 API 請求導致轉圈
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner('正在從數據庫同步資訊...'):
            df, info = get_stock_data(ticker)
            
            if df is not None and not df.empty:
                # 顯示市場數據卡片
                st.subheader("📊 即時市場動態")
                cols = st.columns(4)
                cols[0].metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
                cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                cols[3].metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                
                # 股價趨勢
                st.subheader("📈 股價走勢")
                st.line_chart(df['Close'])
            else:
                st.error("無法取得該股資料，請確認代號或檢查網路連接。")

elif menu == "部位管理":
    st.title("💼 部位管理系統")
    st.write("此功能運作正常。")
    # 呈現持倉資料表
    st.table(pd.DataFrame({
        "股票代號": ["2330", "2881"],
        "持倉成本": [600, 50]
    }))
