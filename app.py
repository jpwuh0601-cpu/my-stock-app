import streamlit as st
import yfinance as yf
import pandas as pd
import re
from analyzer import generate_ai_analysis

st.set_page_config(page_title="AI 籌碼深度分析看板", layout="wide")

st.title("📈 互動式 AI 籌碼深度分析")

# 增強的代號自動修復邏輯
def format_ticker(ticker_input):
    ticker = ticker_input.strip().upper()
    base = re.sub(r'(TW|TWO)$', '', ticker)
    return f"{base}.TW"

@st.cache_data(ttl=300)
def fetch_stock_data(ticker):
    try:
        formatted = format_ticker(ticker)
        stock = yf.Ticker(formatted)
        info = stock.info
        if 'currentPrice' not in info:
            stock = yf.Ticker(f"{ticker.replace('TW', '').strip()}.TWO")
            info = stock.info
        return info, formatted
    except Exception:
        return None, ticker

with st.sidebar:
    st.header("自選股設定")
    manual_ticker = st.text_input("輸入股票代號 (如 2330):", value="2330")
    refresh_btn = st.button("即時深度分析")

if refresh_btn:
    with st.spinner(f"正在深度分析..."):
        info, ticker_used = fetch_stock_data(manual_ticker)
        
        if info:
            # 1. 核心指標
            st.success(f"成功取得 {ticker_used} 資料")
            col1, col2, col3 = st.columns(3)
            col1.metric("當前股價", f"{info.get('currentPrice', 'N/A')}")
            col2.metric("本益比 (PE)", f"{info.get('forwardPE', 'N/A')}")
            col3.metric("EPS", f"{info.get('trailingEps', 'N/A')}")
            
            # 2. 呼叫深度分析模組 (此處模擬傳入數據，未來請填入爬蟲抓取的 DataFrame)
            analysis_result = generate_ai_analysis(ticker_used, info)
            
            st.divider()
            
            # 3. 三大法人表格
            st.subheader("🏛️ 三大法人 10 日買賣超明細")
            if not analysis_result['institutional_table'].empty:
                st.dataframe(analysis_result['institutional_table'], use_container_width=True)
            else:
                st.info("尚無法人數據")
                
            # 4. 券商表格
            st.subheader("🏢 10 家券商 10 日買賣超細項")
            if not analysis_result['broker_table'].empty:
                st.dataframe(analysis_result['broker_table'], use_container_width=True)
            else:
                st.info("尚無券商分點數據")
                
            # 5. 黑天鵝與 AI 分析
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("🦢 黑天鵝危機警示")
                report = analysis_result['black_swan_report']
                if report['status'] == "⚠️ 警示":
                    st.error(report['report'])
                else:
                    st.success(report['report'])
            
            with col_b:
                st.subheader("🤖 AI 主力分析")
                st.info(analysis_result['main_force_analysis'])
        else:
            st.error(f"❌ 無法取得 {manual_ticker} 資料。")
