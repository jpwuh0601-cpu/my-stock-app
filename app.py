import streamlit as st
import yfinance as yf
import os

# 1. 最嚴謹的設定方式：確保只執行一次且放在最上方
try:
    st.set_page_config(page_title="股市儀表板", layout="wide")
except st.errors.StreamlitAPIException:
    pass

st.title("📈 專業股市決策儀表板")

# 2. 修改為手動輸入模式
ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "").strip().upper()

if ticker_input:
    with st.spinner(f"正在為您查詢 {ticker_input} 的即時數據..."):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            
            # 檢查代號是否有效
            if "currentPrice" not in info:
                st.error("無法找到該股票代號，請確認是否正確 (台股請記得加上 .TW 或 .TWO)。")
            else:
                # 核心指標顯示
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("股價", info.get("currentPrice", 0))
                col2.metric("每股淨值", info.get("bookValue", 0))
                col3.metric("本益比", info.get("trailingPE", 0))
                col4.metric("EPS", info.get("trailingEps", 0))
                
                # 財務預估模型
                st.markdown("---")
                st.subheader("📊 明年財務預估模型")
                
                c1, c2 = st.columns(2)
                margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
                payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
                
                # 計算邏輯 (使用 YFinance 獲取之營收數據)
                est_revenue = info.get("totalRevenue", 1e9) * 1.12
                est_net_profit = est_revenue * margin_rate
                est_eps = est_net_profit / info.get("sharesOutstanding", 1e9)
                est_dividend = est_eps * payout_rate
                
                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
                p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
                p3.metric("預估 EPS", f"{est_eps:.2f}")
                p4.metric("預估現金股利", f"{est_dividend:.2f}")
                
        except Exception as e:
            st.error(f"資料讀取錯誤: {e}")
else:
    st.info("請在上方輸入股票代號以開始查詢。")
