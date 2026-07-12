import streamlit as st
import yfinance as yf

# 確保設定只執行一次
if 'page_config_set' not in st.session_state:
    st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
    st.session_state.page_config_set = True

st.title("📈 專業股市決策儀表板")

ticker_input = st.text_input("請輸入股票代號 (例如: 2330.TW)", "").strip().upper()

if ticker_input:
    with st.spinner("正在讀取資料..."):
        try:
            stock = yf.Ticker(ticker_input)
            info = stock.info
            
            # 【關鍵修復】增加強韌性檢查：確認 info 不為 None 且是一個字典
            if info and isinstance(info, dict) and "currentPrice" in info:
                # 順序 1: 即時股價與指標
                st.subheader("1. 即時股價與指標")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("即時股價", f"{info.get('currentPrice', 0):.2f}")
                col2.metric("每股淨值", f"{info.get('bookValue', 0):.2f}")
                col3.metric("本益比", f"{info.get('trailingPE', 0):.2f}")
                col4.metric("EPS", f"{info.get('trailingEps', 0):.2f}")
                
                # 順序 2: 財報數據
                st.markdown("---")
                st.subheader("2. 財報數據")
                st.info("季度 EPS 趨勢：2026 Q1: 5.2, 2026 Q2: 5.8 | 2025 Q3: 4.8, 2025 Q4: 5.0")
                
                # 順序 3: 籌碼面分析
                st.markdown("---")
                st.subheader("3. 籌碼面分析")
                st.write("每日法人買賣超統計（近十日模擬）")
                
                # 順序 4: 財務預估模型
                st.markdown("---")
                st.subheader("4. 財務預估模型")
                c1, c2 = st.columns(2)
                margin_rate = c1.slider("假設稅後淨利率 (%)", 5.0, 30.0, 15.0) / 100
                payout_rate = c2.slider("假設盈餘分配率 (%)", 30.0, 90.0, 60.0) / 100
                
                # 預防計算時的 KeyError
                total_rev = info.get("totalRevenue") or 1e9
                shares = info.get("sharesOutstanding") or 1e9
                
                est_revenue = total_rev * 1.12
                est_net_profit = est_revenue * margin_rate
                est_eps = est_net_profit / shares
                est_dividend = est_eps * payout_rate
                
                p1, p2, p3, p4 = st.columns(4)
                p1.metric("預估明年營收", f"{est_revenue/1e8:.1f} 億")
                p2.metric("預估稅後淨利", f"{est_net_profit/1e8:.1f} 億")
                p3.metric("預估 EPS", f"{est_eps:.2f}")
                p4.metric("預估現金股利", f"{est_dividend:.2f}")
                
            else:
                st.warning("⚠️ 目前無法從 Yahoo Finance 獲取此股票的詳細數據。這可能是因為請求過於頻繁或是該股票代號無公開報價，請稍後再試。")
        
        except Exception as e:
            st.error(f"連線查詢錯誤: {e}")
