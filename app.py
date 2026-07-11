import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

def fetch_stock_data(ticker):
    # 使用 Yahoo Finance 的輕量級 API 接口，速度最快且不會觸發崩潰
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        result = data['quoteResponse']['result'][0]
        return {
            "price": result.get("regularMarketPrice", 0),
            "change": result.get("regularMarketChangePercent", 0),
            "eps": result.get("trailingEps", 0),
            "pe": result.get("trailingPE", 0),
            "nav": result.get("bookValue", 0),
            "shares": result.get("sharesOutstanding", 0)
        }
    except Exception as e:
        return {"error": str(e)}

st.title("📈 專業股市決策儀表板")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取市場數據..."):
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error("無法取得數據，請確認代號是否正確。")
        else:
            # 即時指標顯示
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{data['price']:.2f}")
            col2.metric("漲跌幅", f"{data['change']:.2f}%")
            col3.metric("EPS", f"{data['eps']:.2f}")
            col4.metric("本益比", f"{data['pe']:.2f}")

            st.divider()

            st.subheader("💡 AI 財務決策估值模型")
            
            # 輸入變數區
            col_a, col_b = st.columns(2)
            yoy = col_a.number_input("最新累計營收年增率 (%)", value=10.0) / 100
            prev_rev = col_b.number_input("上年度營收 (億)", value=1000.0)
            net_margin = col_a.number_input("合適稅後淨利率 (%)", value=20.0) / 100
            payout_ratio = col_b.number_input("合適盈餘分配率 (%)", value=60.0) / 100
            
            # 計算邏輯
            est_rev = prev_rev * (1 + yoy)
            est_net_profit = est_rev * net_margin
            est_eps = (est_net_profit * 100000000) / (data['shares'] if data['shares'] > 0 else 1)
            est_dividend = est_eps * payout_ratio
            
            # 顯示結果
            st.success(f"今年預估營收: {est_rev:.2f} 億 | 預估稅後淨利: {est_net_profit:.2f} 億")
            st.info(f"預估 EPS: {est_eps:.2f} | 預估現金股利: {est_dividend:.2f}")

st.sidebar.markdown("---")
st.sidebar.info("使用 API 輕量化模式，確保系統穩定。")
