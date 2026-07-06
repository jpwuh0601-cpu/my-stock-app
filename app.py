import streamlit as st
import pandas as pd
from worker import fetch_stock_data, fetch_institutional_data, fetch_top_brokers_data

# 頁面配置設定
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")

st.title("📈 個股籌碼分析系統")

# 在函式上方加入快取裝飾器，確保 1 小時內重複查詢不會觸發 API 限制
@st.cache_data(ttl=3600)
def get_data_cached(ticker):
    """取得經過快取處理的資料"""
    return fetch_stock_data(ticker)

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    with st.spinner("正在讀取資料，請稍候..."):
        # 調用快取函式，減少 API 請求頻率
        data = get_data_cached(ticker)
        
        # 錯誤處理
        if data.get("error"):
            st.error(f"系統狀態: {data['error']}")
        else:
            info = data.get("info", {})
            
            # 1. 基礎指標
            st.subheader("1. 股價與基本面")
            c1, c2, c3 = st.columns(3)
            c1.metric("即時股價", f"{info.get('currentPrice', 0):.2f}")
            c2.metric("EPS", f"{data.get('eps', 0):.2f}")
            c3.metric("本益比", f"{info.get('forwardPE', 0):.2f}")

            # 2. 法人與籌碼
            st.subheader("2. 法人籌碼統計 (模擬數據)")
            try:
                inst_df = fetch_institutional_data(ticker)
                st.dataframe(inst_df.set_index("日期"), use_container_width=True)
            except Exception:
                st.warning("法人籌碼數據載入異常。")

            # 3. 新聞區塊 (加入嚴謹的資料型別檢查，避免 key error)
            st.subheader("3. 即時財經新聞")
            news = info.get("news", [])
            if isinstance(news, list) and len(news) > 0:
                for n in news:
                    if isinstance(n, dict) and 'title' in n:
                        st.write(f"- {n['title']}")
            else:
                st.write("目前無最新財經新聞。")

            st.success("✅ 資料更新完成")

# 頁尾提示
st.sidebar.info("提示：若頻繁出現 Too Many Requests，請等待 15 分鐘後再查詢，或檢查程式碼中的 API 延遲設定。")
