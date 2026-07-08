import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="股市隨身看", layout="centered")

# 手機友善 CSS
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def main():
    st.title("📈 股市隨身看")
    data = load_data()

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
        c1.metric("股價", f"{s['price']:.2f}")
        c2.metric("EPS", f"{s['eps']:.2f}")
        
        # 風險評估
        if s.get("black_swan_global") == "⚠️ 警示中":
            st.error(f"風險警示: {', '.join(s.get('black_swan_global_reasons', []))}")
        
        # AI 分析內容
        st.write("---")
        st.markdown("**🤖 AI 深度分析:**")
        st.info(s['ai_report'])
        
        # 最後更新
        st.caption(f"更新於: {s.get('last_update')}")
    else:
        st.warning("查無資料，請確認每日排程是否執行。")

if __name__ == "__main__":
    main()
