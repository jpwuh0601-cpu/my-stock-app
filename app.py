import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 側邊欄搜尋
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)", value="2330")
search_button = st.sidebar.button("開始搜尋")

@st.cache_data(ttl=3600)
def get_stock_data(ticker_code):
    try:
        time.sleep(1)
        ticker = yf.Ticker(f"{ticker_code}.TW")
        info = ticker.info
        hist = ticker.history(period="1mo")
        return info, hist
    except Exception:
        return None, None

# 當按下搜尋按鈕時才執行
if search_button:
    with st.spinner("正在取得數據..."):
        info, hist = get_stock_data(ticker_input)
        
        # --- 關鍵修正：檢查 info 是否為 None ---
        if info is None or not isinstance(info, dict):
            st.error("無法取得該股票資料，請檢查代碼是否正確。")
        else:
            # 安全存取邏輯
            current_price = info.get("currentPrice", 0)
            st.subheader(f"代碼: {ticker_input} 最新價格: {current_price}")

            # 顯示其他數據
            col1, col2, col3 = st.columns(3)
            col1.metric("本益比", info.get("trailingPE", "N/A"))
            col2.metric("EPS", info.get("trailingEps", "N/A"))
            col3.metric("市值", f"{info.get('marketCap', 0)/1e9:.1f} B")
            
            st.success("數據載入成功！")
else:
    st.info("請在左側輸入股票代碼並按下搜尋。")
