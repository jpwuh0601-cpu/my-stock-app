import streamlit as st
import json
import os

# 設定頁面屬性
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

# 設定數據檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "market_data.json")

def load_data():
    """安全讀取 JSON 資料，若讀取失敗返回空字典"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    
    # 載入所有數據
    data = load_data()
    
    # 提取所有股票代號（排除掉 last_updated 或其他系統欄位）
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("系統尚未初始化數據，請等待 GitHub Actions 執行自動化任務。")
        return

    # 初始化 Session State 以儲存選股狀態
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0]

    # 側邊欄控制面板
    with st.sidebar:
        st.subheader("控制面板")
        
        # 下拉選單：強制選取 session_state 中的值
        selected = st.selectbox(
            "請選擇監控標的", 
            tickers, 
            index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0
        )
        
        # 按鈕觸發狀態更新與強制渲染
        if st.button("確認選擇"):
            if st.session_state.selected_ticker != selected:
                st.session_state.selected_ticker = selected
                st.rerun() # 強制重新整理頁面以更新資料

    # 獲取當前選擇標的的詳細資訊
    current_ticker = st.session_state.selected_ticker
    info = data.get(current_ticker, {})
    
    # 邏輯防呆：確認該代號是否有資料結構
    if not info or "price" not in info:
        st.warning(f"標的 {current_ticker} 目前無有效資料，請稍候系統自動更新。")
    else:
        st.header(f"監控標的: {current_ticker}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{info.get('price', 0):,.2f}")
        # 根據您的 market_data.json，history 是一個列表，這裡簡單顯示其長度或最後一筆
        col2.metric("歷史紀錄筆數", len(info.get("history", [])))
        col3.metric("狀態", "已就緒")
        
        st.info(f"AI 分析快評: {info.get('ai_prediction', '無數據')}")
        
    st.caption(f"系統最後更新: {data.get('last_updated', '未知')}")

if __name__ == "__main__":
    main()
