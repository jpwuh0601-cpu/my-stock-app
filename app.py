import streamlit as st
import json
import os

st.set_page_config(page_title="AI 股票分析看板", layout="wide")

@st.cache_data(ttl=3600)
def load_market_data():
    """讀取數據，並確保回傳正確格式"""
    file_path = 'market_data.json'
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception as e:
        st.error(f"讀取 JSON 錯誤: {e}")
        return {}

st.title("📊 每日股票 AI 分析系統")

# 1. 載入數據
data = load_market_data()

# 2. 檢查數據是否為空
if not data:
    st.warning("⚠️ 目前沒有數據，請等待 GitHub Actions 完成分析任務，或確認 market_data.json 是否已生成。")
else:
    # 3. 確保 tickers 清單與 data 對應
    tickers = list(data.keys())
    selected_ticker = st.selectbox("請選擇欲查看的股票代號：", tickers)
    
    # 4. 關鍵防錯：檢查選中的代號是否存在於資料中
    if selected_ticker and selected_ticker in data:
        stock_info = data[selected_ticker]
        
        # 顯示指標 (加入 get 預設值防止 KeyError)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("當前股價", f"{stock_info.get('price', 0)}")
        col2.metric("EPS", f"{stock_info.get('eps', 0)}")
        col3.metric("PE", f"{stock_info.get('pe', 0)}")
        col4.metric("安全等級", f"{stock_info.get('black_swan', '未知')}")
        
        st.markdown("### 💡 AI 分析觀點")
        st.info(stock_info.get('ai_prediction', '無分析數據'))
    else:
        st.error(f"選取的代號 {selected_ticker} 在數據庫中不存在。")

with st.sidebar:
    st.header("系統狀態")
    st.write("已連接至 market_data.json")
