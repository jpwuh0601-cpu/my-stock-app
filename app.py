import streamlit as st
import json
import os

# 設定頁面，將資源載入移至函式內，避免啟動時卡住
st.set_page_config(page_title="AI 股票分析看板", layout="wide")

@st.cache_data(ttl=600) # 增加快取機制，降低頻繁讀取壓力
def load_data():
    """確保檔案讀取過程不會導致程式崩潰"""
    if not os.path.exists('market_data.json'):
        return None
    try:
        with open('market_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

st.title("📊 每日股票 AI 分析系統")

# 讀取數據
data = load_data()

# 處理數據讀取狀態
if data is None:
    st.warning("⚠️ 尚未偵測到市場數據檔 (market_data.json)。請確認 GitHub Actions 是否已執行完畢。")
elif "error" in data:
    st.error(f"⚠️ 讀取數據時發生錯誤: {data['error']}")
else:
    # 只有在資料成功載入時才繪製互動元件
    tickers = list(data.keys())
    if tickers:
        selected_ticker = st.selectbox("請選擇欲查看的股票代號：", tickers)
        stock_info = data.get(selected_ticker, {})
        
        # 顯示指標
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("當前股價", f"{stock_info.get('price', 0)}")
        col2.metric("EPS", f"{stock_info.get('eps', 0)}")
        col3.metric("PE", f"{stock_info.get('pe', 0)}")
        col4.metric("安全等級", f"{stock_info.get('black_swan', '未知')}")
        
        st.markdown("### 💡 AI 分析觀點")
        st.info(stock_info.get('ai_prediction', '無分析數據'))
    else:
        st.info("數據檔案為空，請檢查分析任務。")

with st.sidebar:
    st.write("系統運作中...")
