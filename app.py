import streamlit as st
import pandas as pd
import yfinance as yf

# 設定頁面風格
st.set_page_config(layout="wide", page_title="AI 專業投資儀表板", page_icon="📈")

# 自定義 CSS - 優化配色與鮮豔度
st.markdown("""
    <style>
    .metric-card { 
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%);
        padding: 25px; 
        border-radius: 20px; 
        border-left: 10px solid #2563EB;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    h3 { color: #1E3A8A; font-weight: 800; }
    .stButton>button { border-radius: 12px; background-color: #2563EB; color: white; font-weight: bold; }
    .stMetric { background-color: #fff; padding: 15px; border-radius: 10px; border: 1px solid #e5e7eb; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 AI 專業投資決策中樞 (專業版)")

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

menu = st.sidebar.radio("導航目錄", ["🤖 個股深度分析", "💼 部位管理"])

if menu == "🤖 個股深度分析":
    st.subheader("個股即時數據健檢")
    t = st.text_input("輸入股票代號 (例如 2330)", "2330")
    
    if st.button("啟動專業分析"):
        try:
            ticker_formatted = t.strip() + ".TW" if not any(x in t for x in [".TW", ".TWO"]) else t.strip()
            stock = yf.Ticker(ticker_formatted)
            hist = stock.history(period="6mo")
            info = stock.info
            
            # 技術指標計算 (僅保留 RSI)
            rsi_val = calculate_rsi(hist).iloc[-1]
            
            curr = info.get('currentPrice') or info.get('regularMarketPrice', 0.0)
            eps = info.get('trailingEps', 0.0)
            pe = info.get('trailingPE', 0.0)
            shares = info.get('sharesOutstanding') or 100000000.0
            prev_revenue = info.get('totalRevenue') or 1000000000.0 

            st.markdown("### 📊 即時市場動態")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("即時股價", f"{curr:.2f}")
            col2.metric("RSI (14日)", f"{rsi_val:.2f}")
            col3.metric("EPS", f"{eps:.2f}")
            col4.metric("本益比", f"{pe:.2f}")
            
            # 僅保留 RSI 風險評估
            st.markdown("### 🔍 技術面風險評估")
            if rsi_val > 70: st.warning("⚠️ RSI 過熱：目前股價進入超買區，需留意短期回調風險。")
            elif rsi_val < 30: st.success("✅ RSI 超賣：可能存在反彈機會，建議觀察買入訊號。")
            else: st.info("ℹ️ RSI 處於正常區間，市場趨勢平穩。")

            st.divider()

            # 推算邏輯區塊
            st.markdown("### 🔮 明年專業推算數據 (八步驟邏輯)")
            with st.expander("📝 調整參數 (若自動抓取為 0，請手動修正)", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                manual_prev_revenue = c1.number_input("上年度營收 (元)", value=float(prev_revenue), step=1e7)
                yoy = c2.number_input("累積營收年增率 (%)", value=10.0) / 100
                margin = c3.number_input("稅後淨利率 (%)", value=15.0) / 100
                payout = c4.number_input("盈餘分配率 (%)", value=60.0) / 100
                
                c5, c6 = st.columns(2)
                target_pe = c5.number_input("預期本益比 (P/E)", value=float(pe) if pe and pe > 0 else 15.0)
                manual_shares = c6.number_input("發行股數", value=float(shares), step=1e6)
            
            est_revenue = manual_prev_revenue * (1 + yoy)
            est_net_profit = est_revenue * margin
            est_eps = est_net_profit / manual_shares if manual_shares > 0 else 0
            est_dividend = est_eps * payout
            est_price = est_eps * target_pe

            p1, p2, p3, p4 = st.columns(4)
            p1.metric("預估明年股價", f"{est_price:.2f}")
            p2.metric("預估 EPS", f"{est_eps:.2f}")
            p3.metric("預估現金股利", f"{est_dividend:.2f}")
            p4.metric("預估今年營收", f"{est_revenue/1e9:.2f} B")

            if not hist.empty:
                st.markdown("### 📈 股價走勢")
                st.line_chart(hist['Close'], width='stretch')

        except Exception as e:
            st.error(f"分析過程錯誤: {e}")

elif menu == "💼 部位管理":
    st.subheader("💼 我的持股管理")
    st.info("此區塊目前正在建構中...")
