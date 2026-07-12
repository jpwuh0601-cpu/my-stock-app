import streamlit as st
import yfinance as yf

# 使用 session_state 來確保 set_page_config 只執行一次，徹底解決錯誤
if 'page_config_set' not in st.session_state:
    st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
    st.session_state.page_config_set = True

st.title("📈 專業股市決策儀表板")

# 使用者輸入區
ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "").strip().upper()

if ticker_input:
    with st.spinner("正在讀取資料..."):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            
            # 增加更詳盡的檢查邏輯
            if info and isinstance(info, dict) and "currentPrice" in info:
                # 核心指標
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("即時股價", f"{info.get('currentPrice', 0):.2f}")
                col2.metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                col3.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                col4.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                
                # 財務預估模型
                st.markdown("---")
                st.subheader("📊 明年財務預估模型")
                
                c1, c2 = st.columns(2)
                margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
                payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
                
                # 計算邏輯 (使用安全獲取，避免 KeyError)
                revenue = info.get("totalRevenue") or 1e9
                shares = info.get("sharesOutstanding") or 1e9
                
                est_revenue = revenue * 1.12
                est_net_profit = est_revenue * margin_rate
                est_eps = est_net_profit / shares
                est_dividend = est_eps * payout_rate
                
                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
                p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
                p3.metric("預估 EPS", f"{est_eps:.2f}")
                p4.metric("預估現金股利", f"{est_dividend:.2f}")
            else:
                st.error("找不到代號數據，請確認代號是否包含 .TW 或 .TWO (若為台股)。若錯誤持續發生，請確認 yfinance 套件是否安裝成功。")
        except Exception as e:
            st.error(f"連線查詢錯誤，請確認網路連線或代號是否正確: {e}")
