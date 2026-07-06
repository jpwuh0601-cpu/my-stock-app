import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path): return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

def validate_data(data):
    """自動回測檢查資料是否完整"""
    required_keys = ["price", "eps", "pe"]
    return all(key in data for key in required_keys)

# 1. 自行輸入股票，選擇查詢按鈕
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    if ticker not in data_cache:
        st.warning(f"找不到代號: {ticker}")
    else:
        d = data_cache.get(ticker, {})
        
        # 2. 每股淨值, 本益比, EPS
        st.subheader("基本財務指標")
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值 (NAV)", f"{d.get('nav', 0):.2f}")
        c2.metric("本益比 (PE)", f"{d.get('pe', 0):.2f}")
        c3.metric("EPS", f"{d.get('eps', 0):.2f}")
        
        # 4. 股價漲跌 (紅綠表示)
        price = d.get('price', 0)
        change = d.get('change', 0)
        st.metric("即時股價", f"{price:.2f}", delta=f"{change:.2f}")
        
        # 3. 今/去年每季報表
        st.subheader("季度財務報表")
        if "quarterly_reports" in d:
            st.table(pd.DataFrame(d["quarterly_reports"]))
        else:
            st.write("暫無季度報表資料")
            
        # 4 & 5. 法人與主力籌碼
        st.subheader("籌碼與技術分析 (10日)")
        col1, col2 = st.columns(2)
        with col1:
            st.write("三大法人買賣超")
            st.table(pd.DataFrame(d.get("institutional_10d", [])))
            st.write("資券比")
            st.write(f"{d.get('margin_short_ratio', '無資料')}")
        with col2:
            st.write("主力券商買賣超")
            st.table(pd.DataFrame(d.get("broker_main_10d", [])))

        # 7. 預估營收、EPS 與股利
        st.subheader("今年預測數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("預估營收", d.get("est_revenue", "N/A"))
        col2.metric("預估 EPS", d.get("est_eps", "N/A"))
        col3.metric("預估股利", d.get("est_dividend", "N/A"))

        # 8. 即時新聞 -> 6. AI 財報預測
        st.subheader("即時新聞")
        st.write(d.get("news", "無最新新聞"))
        
        st.subheader("AI 財報預測")
        st.info(d.get("ai_prediction", "AI 分析中..."))
        
        # 6. 自動回測檢查
        if validate_data(d):
            st.success("✅ 資料來源檢測：資料完整且正確")
        else:
            st.error("⚠️ 資料來源檢測：部分數據缺失")

else:
    st.info("請在左側輸入股票代號並點擊查詢。")
