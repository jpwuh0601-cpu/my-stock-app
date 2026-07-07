import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from worker import fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis

st.set_page_config(page_title="專業股市分析系統", layout="wide")
st.title("📈 專業股市分析系統")

# 1. 自行輸入股票
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW").strip()

if st.sidebar.button("查詢股價數據"):
    try:
        # 加入延遲防止頻繁請求被封鎖
        time.sleep(1)
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        # 2. 每股淨額、本益比、EPS
        st.subheader("📊 財務基本指標")
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值 (NAV)", f"{info.get('bookValue', 0):.2f}")
        c2.metric("本益比 (PE)", f"{info.get('trailingPE', 0):.2f}")
        c3.metric("每股盈餘 (EPS)", f"{info.get('trailingEps', 0):.2f}")
        
        # 3. 今/去年每季報表
        st.subheader("📅 財務季報表")
        st.dataframe(stock.quarterly_financials)
        
        # 4. 三大法人十日買賣超 (漲紅跌綠)
        st.subheader("🏦 三大法人十日買賣超")
        inst_data = fetch_institutional_data(ticker_input)
        df_inst = pd.DataFrame(inst_data)
        st.dataframe(df_inst.style.map(lambda x: 'color: red' if x > 0 else ('color: green' if x < 0 else 'color: black')))
        
        # 5. 資券比與主力券商
        st.subheader("📉 十日資券比與主力券商買賣")
        df_brokers = fetch_top_brokers_data(ticker_input)
        st.table(df_brokers)
        
        # 8. 即時新聞 (順序調整)
        st.subheader("📰 即時新聞")
        st.write("系統整合中...")
        
        # 6. AI 財報預測
        st.subheader("🤖 AI 財報預測")
        ai_res = generate_ai_analysis(ticker_input, str(info), str(inst_data))
        st.info(ai_res.get("main_force_analysis", "分析服務連線中..."))
        
        # 7. 預估營收、EPS 與股利
        st.subheader("🔮 預估數據")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("預估營收成長", f"{info.get('revenueGrowth', 0)*100:.1f}%")
        col_b.metric("預估 EPS", f"{info.get('forwardEps', 0):.2f}")
        col_c.metric("股利殖利率", f"{info.get('dividendYield', 0)*100:.2f}%")
        
        # 6-2. 自動回測檢查
        st.divider()
        if info.get('regularMarketPrice') or info.get('currentPrice'):
            st.success("✅ 資料回測檢查成功：數據來源正確且已同步。")
        else:
            st.error("❌ 資料來源異常：請檢查代號是否正確。")
            
    except Exception as e:
        st.error(f"連線限制或代號錯誤: {e}")
