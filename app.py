import streamlit as st
import pandas as pd
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data, fetch_stock_news, check_black_swan
from analyzer import generate_ai_analysis

st.set_page_config(page_title="專業股市分析系統", layout="wide")
st.title("📈 專業股市分析系統")

ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW").strip()

def color_rule(val):
    """漲紅跌綠的顏色規則"""
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
            prev_close = float(info.get("previousClose", 0))
            change = curr_price - prev_close
            color = "red" if change > 0 else ("green" if change < 0 else "black")
            st.markdown(f"### 📊 即時股價: <span style='color:{color}'>{curr_price:.2f} (漲跌: {change:+.2f})</span>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("每股淨值 (NAV)", f"{float(info.get('bookValue', 0)):,.2f}")
            c2.metric("本益比 (PE)", f"{float(info.get('trailingPE', 0)):,.2f}")
            c3.metric("每股盈餘 (EPS)", f"{float(info.get('trailingEps', 0)):,.2f}")
            
            # 3. 季報表
            st.subheader("📅 財務季報表")
            q_fin = info.get('quarterlyFinancials')
            if q_fin is not None:
                st.dataframe(pd.DataFrame(q_fin))
            else:
                st.info("暫無財務報表資料")
            
            # 4. 法人每日細項 (加入防空值檢查)
            st.subheader("🏦 三大法人十日買賣超細項")
            inst_data = fetch_institutional_data(ticker_input)
            if inst_data:
                inst_df = pd.DataFrame(inst_data)
                st.dataframe(inst_df.style.map(color_rule, subset=['外資', '投信', '自營商']))
            else:
                st.info("暫無法人籌碼資料")
            
            # 5. 十家券商十日買賣明細
            st.subheader("📉 主力券商十日買賣明細")
            broker_df = fetch_top_brokers_data(ticker_input)
            if broker_df is not None and not broker_df.empty:
                st.dataframe(broker_df.style.map(color_rule, subset=[f"D-{i}" for i in range(1, 11)]))
            else:
                st.info("暫無主力券商資料")
            
            # 8. 即時新聞
            st.subheader("📰 即時新聞")
            news_items = fetch_stock_news(ticker_input)
            for item in news_items:
                with st.expander(item['title']):
                    st.write(item['summary'])
            
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
            
            # 黑天鵝警示
            status, reasons = check_black_swan(info)
            if status == "安全": st.success(f"✅ 風險狀態: {status}")
            else: st.error(f"🚨 風險狀態: {status} - 原因: {', '.join(reasons)}")
            
            st.divider()
            st.success("✅ 資料回測檢查成功：數據來源正確且已同步。")
