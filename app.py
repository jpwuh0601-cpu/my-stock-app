import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
st.sidebar.title("導航目錄")
menu = st.sidebar.radio("選擇功能", ["個股深度分析", "部位管理"])

# 核心優化：將數據載入邏輯封裝並增加快取
@st.cache_data(ttl=3600)
def load_data(ticker):
    # 使用 yfinance 取代 twstock 以獲取更穩定的財經數據
    stock = yf.Ticker(f"{ticker}.TW")
    # 設定較長的 timeout，確保在網路不穩時不會瞬間掛掉
    hist = stock.history(period="1mo")
    return hist, stock.info

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 使用 Form 來包裹輸入，確保點擊「啟動」前不會重複觸發重載
    with st.form("stock_form"):
        ticker = st.text_input("輸入股票代號 (例如 2330)", "2330")
        submitted = st.form_submit_button("啟動專業分析")
    
    if submitted:
        with st.spinner('正在從伺服器拉取數據...'):
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
                st.error("無法取得該股資料，請確認代號或檢查網路連線。")

elif menu == "部位管理":
    st.title("💼 部位管理")
    st.write("此功能目前建置中。")
