import streamlit as st
import pandas as pd
import requests

# 1. 介面設定 - 確保在最開頭
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 2. 數據獲取函式 - 使用 cache，且確保只在按鈕按下時執行
@st.cache_data(ttl=300)
def fetch_stock_data(ticker):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if 'quoteResponse' in data and data['quoteResponse'].get('result'):
            result = data['quoteResponse']['result'][0]
            return {
                "price": result.get("regularMarketPrice", 0),
                "change": result.get("regularMarketChangePercent", 0),
                "eps": result.get("trailingEps", 0),
                "pe": result.get("trailingPE", 0),
                "nav": result.get("bookValue", 0),
                "shares": result.get("sharesOutstanding", 0)
            }
        return {"error": "找不到股票代號"}
    except Exception as e:
        return {"error": str(e)}

# 3. UI 呈現
st.title("📈 專業股市決策儀表板")

# 側邊欄定義
st.sidebar.header("📊 輸入參數")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

st.sidebar.subheader("💡 AI 財務估值模型參數")
yoy = st.sidebar.number_input("1. 最新累積營收年增率 (%)", value=10.0) / 100
prev_rev = st.sidebar.number_input("2. 上年度營收 (億)", value=1000.0)
net_margin = st.sidebar.number_input("4. 合適稅後淨利率 (%)", value=20.0) / 100
payout_ratio = st.sidebar.number_input("7. 合適盈餘分配率 (%)", value=60.0) / 100

# 執行查詢
if st.sidebar.button("查詢並執行分析"):
    with st.spinner("正在讀取市場數據..."):
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error(f"錯誤: {data['error']}")
        else:
            # 顯示指標
            cols = st.columns(5)
            cols[0].metric("即時股價", f"{data['price']:.2f}")
            cols[1].metric("漲跌幅", f"{data['change']:.2f}%")
            cols[2].metric("EPS", f"{data['eps']:.2f}")
            cols[3].metric("本益比", f"{data['pe']:.2f}")
            cols[4].metric("每股淨值", f"{data['nav']:.2f}")

            # 計算模型
            est_rev = prev_rev * (1 + yoy)
            est_net_profit = est_rev * net_margin
            shares = data['shares']
            est_eps = (est_net_profit * 100000000) / (shares if shares > 0 else 1)
            est_dividend = est_eps * payout_ratio

            st.divider()
            st.subheader("📋 8 大步驟財務模型計算結果")
            
            res1, res2 = st.columns(2)
            res1.metric("今年預估營收 (億)", f"{est_rev:.2f}")
            res1.metric("預估稅後淨利 (億)", f"{est_net_profit:.2f}")
            res2.metric("預估 EPS", f"{est_eps:.2f}")
            res2.metric("預估現金股利", f"{est_dividend:.2f}")
            
            st.info(f"發行股數: {shares:,} 股")

st.sidebar.markdown("---")
st.sidebar.success("系統準備就緒")
