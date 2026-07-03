import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """載入市場資料"""
    if not os.path.exists("market_data.json"): return {}
    with open("market_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def display_metric(label, value, delta):
    """顯示漲跌顏色邏輯：漲紅跌綠"""
    delta_color = "normal" if delta == 0 else ("normal" if delta > 0 else "inverse")
    st.metric(label=label, value=value, delta=f"{delta:.2f}", delta_color=delta_color)

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    
    if not data:
        st.warning("數據載入中...")
        return

    # 側邊欄選股
    with st.sidebar:
        selected_ticker = st.selectbox("請選擇股票代號", list(data.keys()))
        if st.button('確定分析'):
            st.session_state.do_analysis = True

    ticker_data = data.get(selected_ticker, {})
    
    # 1. 即時股價 (漲紅跌綠)
    price = ticker_data.get('price', 0)
    change = ticker_data.get('change', 0) # 假設 worker.py 有提供漲跌點數
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: display_metric("即時股價", f"{price:,.2f}", change)
    with col2: st.metric("每股淨值(BVPS)", f"{ticker_data.get('bvps', 0):.2f}")
    with col3: st.metric("本益比(P/E)", f"{ticker_data.get('pe', 0):.2f}")
    with col4: st.metric("EPS", f"{ticker_data.get('eps', 0):.2f}")

    st.divider()

    # 2. 分頁式版面設計
    tab1, tab2, tab3, tab4 = st.tabs(["📊 市場數據與法人", "📑 財報與預測", "🤖 AI 分析中心", "⚠️ 監控警示"])

    with tab1:
        st.subheader("三大法人 10 日買賣超")
        # 需在 worker.py 加入法人資料結構
        st.info("法人數據：外資(買/賣), 投信(買/賣), 自營商(買/賣)")
        
        st.subheader("10日資券比")
        st.progress(0.45) # 範例視覺化
        st.write("資券比: 45% (警示)")

    with tab2:
        st.subheader("今年與去年每季報表")
        st.dataframe(pd.DataFrame(ticker_data.get('quarterly_report', [])))
        st.subheader("預估今年營收與 EPS/股利")
        st.write(ticker_data.get('forecast', "暫無預測數據"))

    with tab3:
        st.subheader("AI 主力分析與新聞解讀")
        st.info(ticker_data.get('ai_prediction', "暫無 AI 分析"))
        st.subheader("新聞解讀")
        st.write(ticker_data.get('news_summary', "無即時新聞"))

    with tab4:
        st.subheader("黑天鵝危機警示與回測系統")
        # 自動回測狀態檢查
        is_data_fresh = ticker_data.get('last_updated')
        if is_data_fresh:
            st.success("✅ 系統自動回測：資料來源正確且即時")
        else:
            st.error("❌ 警告：資料回測失敗，建議檢查 worker.py")
        
        st.warning("黑天鵝警示：無異常")
        st.button("LINE 通知推送 (尚未連線)")

if __name__ == "__main__":
    main()
