import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="即時投資決策儀表板", layout="wide")

st.title("📈 即時投資決策儀表板")

# 側邊欄：搜尋區
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代號 (例如: 2330)", value="2330")

def get_stock_data(ticker_code):
    """即時呼叫 yfinance 獲取數據"""
    try:
        ticker = yf.Ticker(f"{ticker_code}.TW")
        info = ticker.info
        hist = ticker.history(period="6mo")
        return info, hist
    except Exception as e:
        return None, None

if ticker_input:
    with st.spinner(f"正在載入 {ticker_input} 的即時數據..."):
        info, hist = get_stock_data(ticker_input)
        
        if info and "currentPrice" in info:
            st.subheader(f"代號: {ticker_input} - {info.get('longName', '')}")
            
            # 指標顯示
            col1, col2, col3 = st.columns(3)
            col1.metric("即時股價", value=f"${info.get('currentPrice', 0):,.2f}")
            col2.metric("每股淨值 (BVPS)", value=f"${info.get('bookValue', 0):,.2f}")
            col3.metric("市值", value=f"{info.get('marketCap', 0):,.0f}")

            st.divider()

            tab1, tab2 = st.tabs(["財務與基本面", "技術走勢"])
            
            with tab1:
                st.write("### 基本資料")
                data_df = pd.DataFrame({
                    "項目": ["產業", "本益比", "股息殖利率"],
                    "數值": [info.get('sector', 'N/A'), info.get('trailingPE', 0), f"{info.get('dividendYield', 0)*100:.2f}%"]
                })
                st.table(data_df)
            
            with tab2:
                st.write("### 近六個月股價走勢")
                if hist is not None:
                    st.line_chart(hist['Close'])
                else:
                    st.warning("無法取得技術數據。")
        else:
            st.error("查無此股票代號，請確認輸入格式是否正確（僅支援台股）。")
else:
    st.info("請在左側輸入台股代號以開始查詢。")
