import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="股市決策系統", layout="wide")

# 側邊欄導航
menu = st.sidebar.radio("導航目錄", ["個股深度分析", "部位管理"])

# 確保快取，避免重複請求
@st.cache_data(ttl=3600)
def get_data(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.TW")
        return stock.history(period="1mo"), stock.info
    except Exception:
        return None, None

if menu == "個股深度分析":
    st.title("📈 AI 專業投資決策中樞")
    
    # 強制使用 Form，這是防止轉圈的黃金法則
    with st.form("input_form"):
        ticker = st.text_input("輸入股票代號", "2330")
        submit = st.form_submit_button("執行分析")
    
    if submit:
        with st.spinner("獲取數據中..."):
            df, info = get_data(ticker)
            if df is not None and not df.empty:
                cols = st.columns(4)
                cols[0].metric("股價", f"{df['Close'].iloc[-1]:.2f}")
                cols[1].metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                cols[2].metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                cols[3].metric("淨值", f"{info.get('bookValue', 0):.2f}")
                st.line_chart(df['Close'])
            else:
                st.error("無法載入資料，請確認代號。")

elif menu == "部位管理":
    st.title("💼 部位管理")
    st.table(pd.DataFrame({"代號": ["2330"], "成本": [600]}))
