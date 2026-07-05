import streamlit as st
import json
import os

# 設定頁面標題與佈局
st.set_page_config(page_title="AI 股票分析看板", layout="wide")

@st.cache_data(ttl=3600) # 快取 1 小時，減少重複讀取造成的 Loading 卡死
def load_market_data():
    """強化版數據載入，加入錯誤保護"""
    file_path = 'market_data.json'
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

st.title("📊 每日股票 AI 分析系統")
st.markdown("---")

data = load_market_data()

# 錯誤與載入狀態處理
if data is None:
    st.error("⚠️ 找不到數據檔 (market_data.json)，請確認 GitHub Actions 是否執行成功。")
elif "error" in data:
    st.error(f"⚠️ 數據讀取異常: {data['error']}")
else:
    # 成功載入後顯示介面
    tickers = list(data.keys())
    selected_ticker = st.selectbox("請選擇欲查看的股票代號：", tickers)
    
    stock_info = data[selected_ticker]
    
    # 顯示指標
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("當前股價", f"{stock_info.get('price', 0)}")
    col2.metric("EPS", f"{stock_info.get('eps', 0)}")
    col3.metric("PE", f"{stock_info.get('pe', 0)}")
    col4.metric("安全等級", f"{stock_info.get('black_swan', '未知')}")
    
    st.markdown("### 💡 AI 分析觀點")
    st.info(stock_info.get('ai_prediction', '無分析數據'))
    
    st.markdown("### 📰 最新資訊摘要")
    st.write(stock_info.get('news', '暫無資訊'))

# 側邊欄狀態
with st.sidebar:
    st.header("系統狀態")
    if data and "error" not in data:
        st.success("數據讀取正常")
    else:
        st.error("讀取失敗，請檢查 GitHub Action")
