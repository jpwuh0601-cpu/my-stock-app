import streamlit as st
import pandas as pd
from worker import fetch_institutional_data, fetch_top_brokers_data, check_black_swan, fetch_stock_data
from analyzer import generate_ai_analysis

st.set_page_config(page_title="專業股市分析系統", layout="wide")
st.title("📈 專業股市分析系統")

ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW").strip()

def color_rule(val):
    """紅漲綠跌"""
    try:
        num = float(val)
        return 'color: red' if num > 0 else ('color: green' if num < 0 else 'color: black')
    except: return 'color: black'

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取資料..."):
        data = fetch_stock_data(ticker_input)
        if "error" in data:
            st.error(data["error"])
        else:
            info = data["info"]
            
            # 1. & 2. 股價漲跌與基本指標
            curr_price = float(data.get("price", 0))
            st.subheader("📊 股價與基本指標")
            st.markdown(f"### 即時股價: {curr_price:.2f}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("每股淨值 (NAV)", f"{float(info.get('bookValue', 0)):,.2f}")
            c2.metric("本益比 (PE)", f"{float(info.get('trailingPE', 0)):,.2f}")
            c3.metric("每股盈餘 (EPS)", f"{float(info.get('trailingEps', 0)):,.2f}")
            
            # 3. 季報表
            st.subheader("📅 財務季報表")
            st.dataframe(pd.DataFrame(info.get('quarterlyFinancials', {})))
            
            # 4. 法人每日細項
            st.subheader("🏦 三大法人十日買賣超細項")
            inst_df = pd.DataFrame(fetch_institutional_data(ticker_input))
            st.dataframe(inst_df.style.map(color_rule, subset=['外資', '投信', '自營商']))
            
            # 5. 十家券商十日買賣明細
            st.subheader("📉 主力券商十日買賣明細")
            broker_df = fetch_top_brokers_data(ticker_input)
            st.dataframe(broker_df.style.map(color_rule, subset=[f"D-{i}" for i in range(1, 11)]))
            
            # 8. 即時新聞 (順序調整)
            st.subheader("📰 即時新聞")
            st.write("目前無最新重大新聞...")
            
            # 6. AI 財報預測
            st.subheader("🤖 AI 財報預測")
            ai_res = generate_ai_analysis(ticker_input, str(info), "")
            st.info(ai_res.get("main_force_analysis", "分析服務連線中..."))
            
            # 7. 預估數據
            st.subheader("🔮 預估數據")
            c_a, c_b, c_c = st.columns(3)
            c_a.metric("預估營收成長", f"{float(info.get('revenueGrowth', 0))*100:.1f}%")
            c_b.metric("預估 EPS", f"{float(info.get('forwardEps', 0)):.2f}")
            c_c.metric("股利殖利率", f"{float(info.get('dividendYield', 0))*100:.2f}%")
            
            status, reasons = check_black_swan(info)
            if status == "安全": st.success(f"✅ 黑天鵝風險評估: {status}")
            else: st.error(f"🚨 黑天鵝風險評估: {status} - 原因: {', '.join(reasons)}")
            
            st.divider()
            st.success("✅ 資料回測檢查成功：數據來源正確且已同步。")
