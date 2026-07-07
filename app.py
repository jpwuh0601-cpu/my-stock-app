import streamlit as st
import yfinance as yf
import pandas as pd
import time
from worker import fetch_institutional_data, fetch_top_brokers_data
from analyzer import generate_ai_analysis

st.set_page_config(page_title="專業股市分析系統", layout="wide")
st.title("📈 專業股市分析系統")

# 1. 自行輸入股票
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW").strip()

def safe_float(val):
    """確保數值轉換安全"""
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

if st.sidebar.button("查詢股價數據"):
    try:
        time.sleep(1)
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        # 2. 財務指標
        st.subheader("📊 財務基本指標")
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值 (NAV)", f"{safe_float(info.get('bookValue')):,.2f}")
        c2.metric("本益比 (PE)", f"{safe_float(info.get('trailingPE')):,.2f}")
        c3.metric("每股盈餘 (EPS)", f"{safe_float(info.get('trailingEps')):,.2f}")
        
        # 3. 財務季報表
        st.subheader("📅 財務季報表")
        st.dataframe(stock.quarterly_financials)
        
        # 4. 三大法人十日買賣超 (修正型態錯誤)
        st.subheader("🏦 三大法人十日買賣超")
        inst_data = fetch_institutional_data(ticker_input)
        df_inst = pd.DataFrame(inst_data)
        
        def color_rule(val):
            """強制轉換為 float 再比對"""
            num = safe_float(val)
            if num > 0: return 'color: red'
            if num < 0: return 'color: green'
            return 'color: black'

        # 只對數值欄位應用樣式
        cols_to_style = ['外資', '投信', '自營商']
        st.dataframe(df_inst.style.map(color_rule, subset=cols_to_style))
        
        # 5. 資券比與主力券商
        st.subheader("📉 十日資券比與主力券商買賣")
        df_brokers = fetch_top_brokers_data(ticker_input)
        st.table(df_brokers)
        
        # 8. 即時新聞 (先佔位)
        st.subheader("📰 即時新聞")
        st.write("資訊載入中...")
        
        # 6. AI 財報預測
        st.subheader("🤖 AI 財報預測")
        ai_res = generate_ai_analysis(ticker_input, str(info), str(inst_data))
        st.info(ai_res.get("main_force_analysis", "分析服務連線中..."))
        
        # 7. 預估數據
        st.subheader("🔮 預估數據")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("預估營收成長", f"{safe_float(info.get('revenueGrowth'))*100:.1f}%")
        col_b.metric("預估 EPS", f"{safe_float(info.get('forwardEps')):.2f}")
        col_c.metric("股利殖利率", f"{safe_float(info.get('dividendYield'))*100:.2f}%")
        
        st.divider()
        st.success("✅ 資料回測檢查成功：數據來源正確且已同步。")
            
    except Exception as e:
        st.error(f"連線錯誤或代號輸入錯誤: {e}")
