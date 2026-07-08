import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="股市隨身看", layout="centered")

# 手機友善 CSS
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def load_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"資料讀取錯誤: {e}")
        return {}

def main():
    st.title("📈 股市隨身看")
    data = load_data()

    if data is None:
        st.warning("⚠️ 系統初始化中，找不到數據檔案，請稍候再試。")
        return

    # 快捷查詢區
    cols = st.columns(3)
    tickers_list = ["2330.TW", "2317.TW", "2454.TW"]
    for i, t in enumerate(tickers_list):
        if cols[i].button(t):
            st.session_state.ticker = t

    ticker = st.text_input("輸入股票代號", value=st.session_state.get("ticker", "2330.TW"))

    if ticker in data:
        s = data[ticker]
        st.subheader(f"📊 {ticker} 分析報告")
        
        # 股價與基本面卡片
        c1, c2 = st.columns(2)
        c1.metric("股價", f"{s.get('price', 0):.2f}")
        c2.metric("EPS", f"{s.get('eps', 0):.2f}")
        
        # 風險評估
        if s.get("black_swan_global") == "⚠️ 警示中":
            st.error(f"風險警示: {', '.join(s.get('black_swan_global_reasons', []))}")
        
        # AI 分析內容
        st.write("---")
        st.markdown("**🤖 AI 深度分析:**")
        st.info(s.get('ai_report', '分析服務連線中...'))
        
        # 最後更新
        st.caption(f"更新於: {s.get('last_update', '未知')}")
    else:
        st.warning("查無資料，請確認每日排程執行狀態。")

if __name__ == "__main__":
    main()
