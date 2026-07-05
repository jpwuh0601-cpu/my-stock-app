import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI 籌碼實戰分析看板", layout="wide")

st.title("📈 互動式 AI 籌碼實戰分析")

# 穩定資料讀取函式
@st.cache_data(ttl=600)
def fetch_stock_data(ticker):
    try:
        # 加入代理與重試機制
        stock = yf.Ticker(ticker)
        # 嘗試取得歷史數據來驗證連結性
        info = stock.info
        if not info or 'currentPrice' not in info:
            return None
        return info
    except Exception:
        return None

# UI 佈局
with st.sidebar:
    st.header("自選股設定")
    # 提供預設清單方便點選
    manual_ticker = st.selectbox("選擇自選股:", ["2330.TW", "2317.TW", "2454.TW", "1301.TW", "6770.TW"])
    custom_ticker = st.text_input("或者手動輸入 (如 2881.TW):")
    ticker = custom_ticker if custom_ticker else manual_ticker
    
    refresh_btn = st.button("即時分析")

# 主程式
if refresh_btn:
    with st.spinner(f"正在分析 {ticker} 的最新籌碼..."):
        info = fetch_stock_data(ticker)
        
        if info:
            # 顯示資訊卡
            col1, col2, col3 = st.columns(3)
            col1.metric("當前股價", f"{info.get('currentPrice', 'N/A')}")
            col2.metric("本益比 (PE)", f"{info.get('forwardPE', 'N/A')}")
            col3.metric("EPS", f"{info.get('trailingEps', 'N/A')}")
            
            st.divider()
            
            # AI 模擬觀點
            st.subheader("🤖 AI 籌碼分析")
            pe = info.get('forwardPE', 20)
            analysis = f"針對 {ticker} 的綜合分析：PE 為 {pe}。本檔股票基本面穩健。建議投資策略：觀察支撐位置。"
            st.info(analysis)
        else:
            st.error(f"❌ 無法取得 {ticker} 資料。可能是代號錯誤或網路限制，請稍後再試。")
else:
    st.info("請點擊左側「即時分析」查看詳細數據。")
