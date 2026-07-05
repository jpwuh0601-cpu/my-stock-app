import streamlit as st
import json
import os

# 設定頁面標題與佈局
st.set_page_config(page_title="每日股票 AI 分析", layout="wide")

def load_market_data():
    """從本地 JSON 檔案讀取數據"""
    file_path = 'market_data.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取數據時發生錯誤: {e}")
            return None
    return None

st.title("📊 每日股票 AI 分析系統")
st.markdown("---")

# 載入數據
data = load_market_data()

if data:
    # 建立下拉選單選擇股票
    tickers = list(data.keys())
    selected_ticker = st.selectbox("請選擇欲查看的股票代號：", tickers)
    
    # 取得選定股票的資料
    stock_info = data[selected_ticker]
    
    # 顯示核心數據指標
    col1, col2, col3 = st.columns(3)
    col1.metric("股價", f"{stock_info.get('price', 'N/A')}")
    col2.metric("EPS", f"{stock_info.get('eps', 'N/A')}")
    col3.metric("本益比 (PE)", f"{stock_info.get('pe', 'N/A')}")
    
    # 顯示 AI 分析觀點
    st.markdown("### 💡 AI 分析觀點")
    st.info(stock_info.get('ai_prediction', '目前暫無分析觀點，請稍候更新。'))
    
    # 顯示最後更新時間（若有的話）
    st.caption(f"數據最後更新於本地分析流程完成時")
else:
    # 顯示錯誤提示
    st.warning("⚠️ 找不到分析數據檔 (market_data.json)。")
    st.info("請確認 GitHub Actions 的自動化任務是否已成功執行並產出檔案。")

# 側邊欄顯示額外資訊
with st.sidebar:
    st.header("系統狀態")
    st.success("自動化分析：已連線")
    st.write("本系統每日自動更新最新股市分析數據。")
