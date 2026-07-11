import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 介面設定
st.set_page_config(page_title="專業股市決策儀表板", layout="wide")

# 2. 強健的數據獲取函式
@st.cache_data(ttl=300)
def fetch_stock_data(ticker):
    # 自動處理代號格式
    clean_ticker = ticker.strip().upper()
    if not clean_ticker.endswith((".TW", ".TWO")):
        clean_ticker += ".TW"
    
    try:
        # 使用 yfinance 穩定抓取
        stock = yf.Ticker(clean_ticker)
        info = stock.info
        
        # 檢查是否有資料
        if not info or "currentPrice" not in info:
        
        return {
            "ticker": clean_ticker,
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChangePercent", 0) * 100,
            "eps": info.get("trailingEps", 0),
            "pe": info.get("trailingPE", 0),
            "nav": info.get("bookValue", 0),
            "shares": info.get("sharesOutstanding", 0)
        }
    except Exception as e:
        return {"error": f"連線異常，請稍後再試。詳細錯誤: {str(e)}"}

# 3. UI 呈現
st.title("📈 專業股市決策儀表板")

st.sidebar.header("📊 輸入參數")
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330)", "2330")

st.sidebar.subheader("💡 AI 財務估值模型參數")
yoy = st.sidebar.number_input("1. 最新累積營收年增率 (%)", value=10.0) / 100
prev_rev = st.sidebar.number_input("2. 上年度營收 (億)", value=1000.0)
net_margin = st.sidebar.number_input("4. 合適稅後淨利率 (%)", value=20.0) / 100
payout_ratio = st.sidebar.number_input("7. 合適盈餘分配率 (%)", value=60.0) / 100

# 執行查詢
if st.sidebar.button("查詢並執行分析"):
    with st.spinner(f"正在讀取 {ticker} 的市場數據..."):
        data = fetch_stock_data(ticker)
        
        if "error" in data:
            st.error(data["error"])
        else:
            # 顯示指標
            st.success(f"成功載入 {data['ticker']} 市場數據")
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
st.sidebar.caption("提示：若仍無法顯示，請檢查股票代號是否已上市。")
