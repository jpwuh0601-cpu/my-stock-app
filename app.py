import streamlit as st
import json
import os

# 1. 頁面設定維持在最前面
st.set_page_config(page_title="AI 股票分析系統", layout="wide")

# 2. 將所有檔案讀取操作放入函式中，避免在應用程式啟動時立刻執行
def get_stock_data():
    if not os.path.exists("market_data.json"):
        return None
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# 3. 執行介面渲染
st.title("📊 每日股票 AI 分析系統")

data = get_stock_data()

if data is None:
    st.warning("⚠️ 系統正在初始化或未找到數據檔，請稍候。")
    # 提供一個簡單的按鈕讓使用者手動檢查
    if st.button("重新載入"):
        st.rerun()
else:
    tickers = list(data.keys())
    if not tickers:
        st.info("目前沒有可顯示的股票數據。")
    else:
        selected_ticker = st.selectbox("請選擇股票：", tickers)
        
        # 顯示該股票的詳細資訊
        stock_info = data.get(selected_ticker, {})
        
        # 顯示基本指標
        cols = st.columns(4)
        cols[0].metric("股價", stock_info.get("price", "N/A"))
        cols[1].metric("EPS", stock_info.get("eps", "N/A"))
        cols[2].metric("PE", stock_info.get("pe", "N/A"))
        cols[3].metric("狀態", stock_info.get("black_swan", "N/A"))
        
        st.subheader("💡 AI 分析預測")
        st.info(stock_info.get("ai_prediction", "暫無分析"))

# 4. 側邊欄顯示
with st.sidebar:
    st.write("系統狀態：線上")
    if st.button("強制重整"):
        st.rerun()
