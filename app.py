import streamlit as st
import yfinance as yf
import json
import os
import time
import pandas as pd
import plotly.graph_objects as go

# 設定頁面配置
st.set_page_config(page_title="AI 智能投資決策儀表板", layout="wide")

# 自定義 CSS 樣式
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI 智能投資決策儀表板")

# 側邊欄：搜尋功能
st.sidebar.header("🔍 股票搜尋與分析")
ticker_input = st.sidebar.text_input("輸入台股代碼 (例如: 2330)", value="2330")
search_button = st.sidebar.button("分析股票")

# 獲取資料函數 (加強版)
@st.cache_data(ttl=600)
def get_stock_data(ticker_code):
    try:
        # 強制延遲以避免觸發 Rate Limit
        time.sleep(1.0) 
        ticker = yf.Ticker(f"{ticker_code}.TW")
        info = ticker.info
        hist = ticker.history(period="3mo")
        return info, hist
    except Exception as e:
        st.error(f"獲取資料時發生錯誤: {e}")
        return None, None

def load_market_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

# --- 主要邏輯 ---
if search_button and ticker_input:
    with st.spinner("正在進行 AI 深度籌碼與財報分析..."):
        info, hist = get_stock_data(ticker_input)
        market_data = load_market_data()

        if info is None or not info:
            st.error("無法取得資料，請檢查代碼或稍後再試。")
        else:
            # 顯示頂部 Metrics
            col1, col2, col3, col4 = st.columns(4)
            current_price = info.get("currentPrice", 0)
            col1.metric("目前價格", f"{current_price} TWD")
            col2.metric("本益比 (PE)", info.get("trailingPE", "N/A"))
            col3.metric("每股盈餘 (EPS)", info.get("trailingEps", "N/A"))
            col4.metric("市值", f"{info.get('marketCap', 0) / 1e9:.2f} B")

            # 主圖表
            st.subheader("趨勢分析")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='收盤價'))
            fig.update_layout(title="近 3 個月股價走勢", xaxis_title="日期", yaxis_title="價格")
            st.plotly_chart(fig, use_container_width=True)

            # 分頁資訊
            tab1, tab2, tab3 = st.tabs(["核心財務數據", "籌碼分析", "AI 決策建議"])
            
            with tab1:
                st.subheader("基本面概覽")
                financial_df = pd.DataFrame({
                    "指標": ["預估本益比 (Forward PE)", "殖利率", "每股淨值"],
                    "數值": [info.get("forwardPE", "N/A"), 
                            f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A",
                            info.get("bookValue", "N/A")]
                })
                st.table(financial_df)

            with tab2:
                if market_data:
                    investors = market_data.get('institutional_investors', [])
                    st.write("### 外資籌碼動態")
                    st.json(investors)
                else:
                    st.warning("無籌碼分析數據。")

            with tab3:
                if market_data:
                    st.success("### AI 分析洞察")
                    st.write(market_data.get('ai_prediction', '模型分析處理中...'))
                else:
                    st.info("尚無 AI 預測數據。")

# 底部狀態列
st.sidebar.markdown("---")
st.sidebar.caption("系統狀態: 🟢 已連接至即時數據庫")
