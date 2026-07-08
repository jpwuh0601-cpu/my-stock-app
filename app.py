import streamlit as st
from worker import fetch_stock_data

# 頁面配置
st.set_page_config(page_title="專業股市決策儀表板", layout="centered")

st.title("📈 專業股市決策儀表板")

# 決策標的輸入區
ticker_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")

# 快取機制：確保 API 呼叫效率，設定 10 分鐘 TTL
@st.cache_data(ttl=600)
def get_data_cached(ticker):
    return fetch_stock_data(ticker)

# 查詢按鈕觸發
if st.button("查詢分析數據"):
    with st.spinner("正在連線 Yahoo Finance 獲取即時數據..."):
        # 呼叫 worker.py 即時查詢
        data = get_data_cached(ticker_input)
        
        # 顯示處理邏輯
        if "error" in data:
            st.error(f"查詢失敗: {data['error']}")
        else:
            st.subheader(f"決策報告：{ticker_input.upper()}")
            
            # 儀表板指標區塊 (使用 Streamlit Metric)
            col1, col2, col3 = st.columns(3)
            col1.metric("即時股價", data.get('price', 0))
            col2.metric("每股淨值 (NAV)", data.get('nav', 0))
            col3.metric("本益比 (PE)", data.get('pe', 0))
            
            # 補充資訊
            st.write(f"每股盈餘 (EPS): {data.get('eps', 0)}")
            st.write(f"今日漲跌幅: {data.get('change', 0)}")
            
            st.success("數據已即時更新。")
            st.info("註：本系統已改採純手動即時查詢模式，不再依賴背景檔案，以解決部署報錯問題。")

# 頁腳說明
st.markdown("---")
st.caption("本儀表板專為台灣股市設計，數據源為 Yahoo Finance 即時行情。")
