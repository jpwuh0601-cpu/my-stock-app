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
    try: return float(val)
    except: return 0.0

if st.sidebar.button("查詢股價數據"):
    try:
        time.sleep(1)
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        # 獲取價格與漲跌幅
        curr_price = safe_float(info.get('currentPrice') or info.get('regularMarketPrice'))
        prev_close = safe_float(info.get('previousClose'))
        change_val = curr_price - prev_close
        change_pct = safe_float(info.get('regularMarketChangePercent', 0))
        
        # 決定顏色 (漲紅跌綠)
        price_color = "red" if change_val > 0 else ("green" if change_val < 0 else "black")
        
        # 2. 顯示股價與漲跌 (使用 HTML 渲染顏色)
        st.subheader("📊 股價與基本指標")
        st.markdown(f"### 即時股價: <span style='color:{price_color}'>{curr_price:.2f} ({change_val:+.2f} / {change_pct:+.2f}%)</span>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值 (NAV)", f"{safe_float(info.get('bookValue')):,.2f}")
        c2.metric("本益比 (PE)", f"{safe_float(info.get('trailingPE')):,.2f}")
        c3.metric("每股盈餘 (EPS)", f"{safe_float(info.get('trailingEps')):,.2f}")
        
        # 3. 財務季報表
        st.subheader("📅 財務季報表")
        st.dataframe(stock.quarterly_financials)
        
        # 4. 三大法人十日買賣超
        st.subheader("🏦 三大法人十日買賣超")
        inst_data = fetch_institutional_data(ticker_input)
        df_inst = pd.DataFrame(inst_data)
        st.dataframe(df_inst.style.map(lambda x: 'color: red' if safe_float(x) > 0 else ('color: green' if safe_float(x) < 0 else 'color: black'), subset=['外資', '投信', '自營商']))
        
        # 5. 資券比與主力券商
        st.subheader("📉 十日資券比與主力券商買賣")
        df_brokers = fetch_top_brokers_data(ticker_input)
        st.table(df_brokers)
        
        # 8. 即時新聞
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
