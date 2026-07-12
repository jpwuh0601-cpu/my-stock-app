import streamlit as st
import os
import sys
import pkg_resources

# 強制設定頁面
st.set_page_config(page_title="股市儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

# 除錯模式：顯示目前 Python 環境安裝的套件
def show_installed_packages():
    st.sidebar.write("### 系統已安裝套件檢查")
    packages = [p.key for p in pkg_resources.working_set]
    if 'yfinance' not in packages:
        st.sidebar.error("❌ 系統偵測到未安裝 yfinance！")
    else:
        st.sidebar.success("✅ yfinance 已安裝")
    st.sidebar.write(f"Python: {sys.version}")

show_installed_packages()

# 核心功能
try:
    import yfinance as yf
    
    ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "").strip().upper()
    if ticker_input:
        with st.spinner("正在查詢..."):
            stock = yf.Ticker(ticker_input)
            info = stock.info
            if "currentPrice" in info:
                # 顯示核心指標
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("即時股價", info.get("currentPrice", 0))
                col2.metric("每股淨值", info.get("bookValue", 0))
                col3.metric("本益比", info.get("trailingPE", 0))
                col4.metric("EPS", info.get("trailingEps", 0))
                
                # 財務預估模型
                st.markdown("---")
                st.subheader("📊 明年財務預估模型")
                
                c1, c2 = st.columns(2)
                margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
                payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
                
                # 計算邏輯
                est_revenue = info.get("totalRevenue", 1e9) * 1.12
                est_net_profit = est_revenue * margin_rate
                est_eps = est_net_profit / info.get("sharesOutstanding", 1e9)
                est_dividend = est_eps * payout_rate
                
                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
                p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
                p3.metric("預估 EPS", f"{est_eps:.2f}")
                p4.metric("預估現金股利", f"{est_dividend:.2f}")
                
            else:
                st.error("查無此代號")
except ImportError:
    st.error("系統嚴重錯誤：yfinance 模組無法載入。請確認 requirements.txt 已正確上傳至根目錄。")
