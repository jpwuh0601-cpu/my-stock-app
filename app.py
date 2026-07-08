import streamlit as st
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

st.title("📈 專業股市決策儀表板")

# 決策標的輸入區：提供預設值
ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

# 快取機制：點擊查詢時才觸發，避免頁面重新整理時重複呼叫
@st.cache_data(ttl=600)
def get_data(ticker):
    return fetch_stock_data(ticker)

if st.button("查詢分析數據"):
    with st.spinner("正在連線 Yahoo Finance 獲取即時數據..."):
        # 直接呼叫 worker.py 中的 fetch_stock_data
        data = get_data(ticker_input)
        
        # 顯示狀態與數據
        if "error" in data:
            st.error(f"查詢失敗: {data['error']}")
        else:
            st.subheader(f"決策報告：{ticker_input.upper()}")
            
            # 儀表板指標區塊
            col1, col2, col3 = st.columns(3)
            col1.metric("即時股價", data.get('price', 0))
            col2.metric("每股淨值", data.get('nav', 0))
            col3.metric("本益比", data.get('pe', 0))
            
            st.write(f"每股盈餘 (EPS): {data.get('eps', 0)}")
            st.write(f"今日漲跌幅: {data.get('change', 0)}")
            
            st.success("數據已即時更新。")
            st.info("註：本系統現已轉為手動即時查詢模式，完全不再依賴背景檔案，運作將非常穩定。")

# 底部頁腳說明
st.markdown("---")
st.caption("本儀表板專為台灣股市設計，數據源為 Yahoo Finance 即時行情。")
