import streamlit as st
import yfinance as yf
import pandas as pd

# 設定頁面基礎配置
st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航 (保留您原本的結構)
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 核心優化：使用快取防止重複聯網請求，設定較長的 TTL
@st.cache_data(ttl=3600)
def load_data(ticker):
    """取得個股資料，移除不必要的外部 API 依賴"""
    stock = yf.Ticker(f"{ticker}.TW")
    # 簡化請求流程
    hist = stock.history(period="1mo")
    return hist, stock.info

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 使用 Form 結構，確保使用者點擊後才觸發請求
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner('正在從財經伺服器拉取數據...'):
            try:
                df, info = load_data(ticker)
                
                if df is not None and not df.empty:
                    # 顯示市場動態
                    cols = st.columns(4)
                    cols[0].metric("即時股價", f"{df['Close'].iloc[-1]:.2f}")
                    cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                    cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                    cols[3].metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                    
                    st.subheader(f"📈 {ticker} 股價走勢")
                    st.line_chart(df['Close'])
                else:
                    st.error("無法取得該股資料，請確認代號正確。")
            except Exception as e:
                st.error(f"連線錯誤，請稍後再試: {e}")

elif menu == "部位管理":
    st.title("💼 部位管理")
    st.write("此功能目前建置中。")
