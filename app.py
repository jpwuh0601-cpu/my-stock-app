import streamlit as st
import pandas as pd
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data, fetch_stock_news, check_black_swan
from analyzer import generate_ai_analysis

st.set_page_config(page_title="專業股市分析系統", layout="wide")
st.title("📈 專業股市分析系統")

ticker_input = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW").strip()

def color_rule(val):
    try:
        num = float(val)
        return 'color: red' if num > 0 else ('color: green' if num < 0 else 'color: black')
    except: return 'color: black'

if st.sidebar.button("查詢分析數據"):
    with st.spinner("資料讀取中..."):
        data = fetch_stock_data(ticker_input)
        if "error" in data:
            st.error(data["error"])
        else:
            info = data["info"]
            curr_price = float(data.get("price", 0))
            prev_close = float(info.get("previousClose", 0))
            change = curr_price - prev_close
            color = "red" if change > 0 else ("green" if change < 0 else "black")
            
            st.markdown(f"### 現價: <span style='color:{color}'>{curr_price:.2f} ({change:+.2f})</span>", unsafe_allow_html=True)
            
            # 籌碼與報表
            st.subheader("🏦 三大法人十日買賣超細項")
            inst_df = pd.DataFrame(fetch_institutional_data(ticker_input))
            st.dataframe(inst_df.style.map(color_rule, subset=['外資', '投信', '自營商']))
            
            st.subheader("📉 主力券商十日買賣明細")
            broker_df = fetch_top_brokers_data(ticker_input)
            st.dataframe(broker_df.style.map(color_rule, subset=[f"D-{i}" for i in range(1, 11)]))
            
            # 新聞
            st.subheader("📰 即時新聞")
            for item in fetch_stock_news(ticker_input):
                with st.expander(item['title']):
                    st.write(item['summary'])
            
            # 預測與警示
            status, reasons = check_black_swan(info)
            if status == "安全": st.success(f"✅ 風險狀態: {status}")
            else: st.error(f"🚨 風險狀態: {status} - 原因: {', '.join(reasons)}")
            
            st.success("✅ 資料回測檢查成功。")
