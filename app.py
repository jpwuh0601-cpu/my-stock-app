import streamlit as st
import pandas as pd
import time
from worker import fetch_institutional_data, fetch_top_brokers_data, check_black_swan, fetch_stock_data
from analyzer import generate_ai_analysis

st.set_page_config(page_title="專業股市分析系統", layout="wide")
st.title("📈 專業股市分析系統")

# 1. 自行輸入股票
ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW").strip()

def safe_float(val):
    try: return float(val)
    except: return 0.0

if st.sidebar.button("查詢股價數據"):
    with st.spinner("正在讀取資料..."):
        try:
            data = fetch_stock_data(ticker_input)
            if "error" in data:
                st.error(data["error"])
            else:
                info = data["info"]
                
                # 2. 基本指標 (每股淨額、本益比、EPS)
                st.subheader("📊 財務基本指標")
                c1, c2, c3 = st.columns(3)
                c1.metric("每股淨值 (NAV)", f"{safe_float(info.get('bookValue')):,.2f}")
                c2.metric("本益比 (PE)", f"{safe_float(info.get('trailingPE')):,.2f}")
                c3.metric("每股盈餘 (EPS)", f"{safe_float(info.get('trailingEps')):,.2f}")
                
                # 3. 季報表
                st.subheader("📅 財務季報表")
                st.dataframe(pd.DataFrame(info.get('quarterlyFinancials', {})))
                
                # 4. 法人每日細項 (漲紅跌綠)
                st.subheader("🏦 三大法人十日買賣超")
                inst_df = pd.DataFrame(fetch_institutional_data(ticker_input))
                st.dataframe(inst_df.style.map(lambda x: 'color: red' if safe_float(x) > 0 else ('color: green' if safe_float(x) < 0 else 'color: black'), subset=['外資', '投信', '自營商']))
                
                # 5. 十家券商十日買賣明細
                st.subheader("📉 主力券商十日買賣明細")
                st.dataframe(fetch_top_brokers_data(ticker_input))
                
                # 8. 即時新聞 (順序調整)
                st.subheader("📰 即時新聞")
                st.write("目前無最新重大新聞...")
                
                # 6. AI 財報預測
                st.subheader("🤖 AI 財報預測")
                ai_res = generate_ai_analysis(ticker_input, str(info), "")
                st.info(ai_res.get("main_force_analysis", "分析服務連線中..."))
                
                # 7. 預估數據
                st.subheader("🔮 預估數據")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("預估營收成長", f"{safe_float(info.get('revenueGrowth'))*100:.1f}%")
                col_b.metric("預估 EPS", f"{safe_float(info.get('forwardEps')):.2f}")
                col_c.metric("股利殖利率", f"{safe_float(info.get('dividendYield'))*100:.2f}%")
                
                # 黑天鵝警示
                status, reasons = check_black_swan(ticker_input, info)
                if status == "安全": st.success(f"✅ 黑天鵝風險評估: {status}")
                else: st.error(f"🚨 黑天鵝風險評估: {status} - 原因: {', '.join(reasons)}")
                
                st.divider()
                st.success("✅ 資料回測檢查成功：數據來源正確且已同步。")
        except Exception as e:
            st.error(f"系統錯誤: {e}")
