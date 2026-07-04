import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from analyzer import get_ai_analysis

st.set_page_config(layout="wide", page_title="即時金融查詢終端")

st.title("🔍 專業金融即時查詢終端")

# 手動輸入模式
input_ticker = st.text_input("請輸入股票代號 (例如: 2330.TW)", placeholder="輸入代號後按下 Enter")

if input_ticker:
    with st.spinner(f"正在即時聯網分析 {input_ticker}..."):
        try:
            ticker = yf.Ticker(input_ticker)
            info = ticker.info
            
            # 檢查代號有效性
            if "currentPrice" not in info:
                st.error("查無此標的，請確認代號是否正確 (台股請加 .TW)")
            else:
                # 顯示即時指標
                col1, col2, col3 = st.columns(3)
                col1.metric("即時價格", f"{info.get('currentPrice', 0):.2f}")
                col2.metric("EPS", info.get("trailingEps", "N/A"))
                col3.metric("本益比", info.get("forwardPE", "N/A"))
                
                # 呼叫分析引擎
                st.subheader("🤖 AI 市場解讀")
                ai_result = get_ai_analysis(input_ticker)
                st.info(ai_result)
                
                # 歷史趨勢圖
                st.subheader("📈 歷史走勢")
                hist = ticker.history(period="1mo")
                st.line_chart(hist['Close'])

        except Exception as e:
            st.error(f"查詢發生錯誤: {e}")

st.sidebar.markdown("### 系統說明")
st.sidebar.write("本系統已切換為「純即時查詢模式」，不再依賴自動排程，所有數據皆為您輸入代號當下聯網讀取。")
