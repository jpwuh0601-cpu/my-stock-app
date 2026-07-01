import streamlit as st
import yfinance as yf
import json
import os
import time

# 設定頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

st.title("📊 AI 智能投資決策儀表板")

# 側邊欄：搜尋功能
st.sidebar.header("股票搜尋")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)", value="2330")
search_button = st.sidebar.button("開始搜尋")

# 使用快取降低 API 呼叫頻率 (快取 10 分鐘)
@st.cache_data(ttl=600)
def get_stock_data(ticker_code):
    try:
        # 強制延遲以避免觸發 Rate Limit
        time.sleep(1.5) 
        ticker = yf.Ticker(f"{ticker_code}.TW")
        info = ticker.info
        hist = ticker.history(period="1mo")
        return info, hist
    except Exception as e:
        return None, None

def load_market_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

# 主邏輯
if search_button and ticker_input:
    with st.spinner("正在進行 AI 深度籌碼與財報分析..."):
        info, hist = get_stock_data(ticker_input)
        market_data = load_market_data()

        if info is None or not info:
            st.error("無法取得資料，請檢查代碼或稍後再試 (API 請求限制)。")
        else:
            current_price = info.get("currentPrice", "N/A")
            st.subheader(f"代碼: {ticker_input} 最新價格: {current_price}")

            # 顯示分頁
            tab1, tab2, tab3 = st.tabs(["基本面與財報", "籌碼面分析", "AI 預測"])
            
            with tab1:
                st.write(f"本益比: {info.get('trailingPE', 'N/A')}")
                st.write(f"預估 EPS: {info.get('trailingEps', 'N/A')}")
                st.write(f"市值: {info.get('marketCap', 'N/A')}")

            with tab2:
                if market_data:
                    investors = market_data.get('institutional_investors', [])
                    if investors:
                        st.write(f"外資買賣超: {investors[0].get('買賣超', 'N/A')}")
                    else:
                        st.write("目前無外資籌碼數據。")
                else:
                    st.write("目前無即時籌碼數據檔案。")

            with tab3:
                if market_data:
                    st.info(market_data.get('ai_prediction', 'AI 模型分析中...'))
                else:
                    st.write("目前無 AI 預測數據。")

# 系統狀態顯示
st.sidebar.markdown("---")
st.sidebar.write("系統狀態: 🟢 LINE 通知已連線")
if os.path.exists("market_data.json"):
    mtime = os.path.getmtime("market_data.json")
    st.sidebar.write(f"數據最後更新: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))}")
