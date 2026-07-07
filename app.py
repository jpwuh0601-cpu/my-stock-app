import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from worker import fetch_institutional_data
from analyzer import generate_ai_analysis

# 設定頁面配置
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# 使用輸入框取代下拉選單
ticker = st.sidebar.text_input("請輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("即時查詢"):
    with st.spinner(f"正在抓取 {ticker} 的資料..."):
        try:
            # 1. 直接即時抓取 Yahoo Finance 資料
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1d")
            last_price = float(hist['Close'].iloc[-1]) if not hist.empty else float(info.get('currentPrice', 0))
            
            # 2. 獲取籌碼資料 (呼叫原本的 worker 函數)
            inst_data = fetch_institutional_data(ticker)
            
            # 3. 生成 AI 分析
            ai_res = generate_ai_analysis(ticker, str(info), str(inst_data))
            
            # 4. 顯示 8 項關鍵數據
            st.subheader(f"📊 {ticker} 即時分析儀表板")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{last_price:.2f}")
            col2.metric("漲跌幅", f"{info.get('regularMarketChangePercent', 0):.2f}%")
            col3.metric("每股淨額", f"{info.get('bookValue', 0):.2f}")
            col4.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
            
            col5, col6, col7, col8 = st.columns(4)
            col5.metric("每股盈餘", f"{info.get('trailingEps', 0):.2f}")
            col6.metric("融資餘額比", "0.00%") 
            
            st.subheader("🤖 AI 分析")
            st.info(ai_res.get("main_force_analysis", "AI 正在分析中..."))
            
            # 5. 籌碼視覺化
            st.subheader("📊 近期法人買賣超")
            if inst_data:
                df = pd.DataFrame(inst_data)
                fig = go.Figure(data=[
                    go.Bar(name='外資', x=df['日期'], y=df['外資']),
                    go.Bar(name='投信', x=df['日期'], y=df['投信']),
                    go.Bar(name='自營商', x=df['日期'], y=df['自營商'])
                ])
                fig.update_layout(barmode='group')
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"查詢失敗，請檢查股票代號是否正確。錯誤訊息: {e}")
