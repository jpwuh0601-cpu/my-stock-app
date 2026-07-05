import streamlit as st
import json
import os

# 設定網頁標題與排版
st.set_page_config(page_title="AI 投資秘書儀表板", layout="wide")
st.title("📈 AI 投資秘書儀表板")

def load_data():
    """從 GitHub Actions 產生的 JSON 檔案載入分析結果"""
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

data = load_data()

if data:
    # 建立左側選單
    tickers = list(data.keys())
    selected_ticker = st.sidebar.selectbox("請選擇分析個股", tickers)
    
    # 顯示分析結果
    ticker_data = data[selected_ticker]
    st.header(f"個股分析: {selected_ticker}")
    
    # 快速看板區域
    col1, col2 = st.columns(2)
    with col1:
        st.metric("目前價格", ticker_data.get('price', 'N/A'))
    
    # AI 報告區塊
    st.subheader("🤖 AI 深度財經分析")
    report = ticker_data.get('ai_report', '尚未進行分析或數據載入中...')
    
    # 根據 AI 報告中的符號進行 UI 顏色強化
    if "⚠️" in report:
        st.warning(report)
    elif "🚀" in report:
        st.success(report)
    else:
        st.markdown(report)
        
    st.divider()
    st.caption("自動化數據更新於 GitHub Actions")
else:
    st.info("系統尚未產生數據，請確認 GitHub Actions 是否已執行完畢。")
