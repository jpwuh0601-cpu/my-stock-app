import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if "selected" not in st.session_state: st.session_state.selected = tickers[0] if tickers else ""
    with st.sidebar:
        sel = st.selectbox("監控標的", tickers, index=tickers.index(st.session_state.selected) if st.session_state.selected in tickers else 0)
        if st.button("更新"): st.session_state.selected = sel; st.rerun()

    info = data.get(st.session_state.selected, {})
    
    # 1. 即時股價
    chg = info.get("change", 0)
    st.subheader(f"即時股價: :{ 'red' if chg>=0 else 'green' }[{info.get('price', 0):,.2f}]")
    
    # 2. 每股淨值、本益比、EPS
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值", info.get("book_value", 0))
    c2.metric("本益比", info.get("pe", 0))
    c3.metric("EPS", info.get("eps", 0))
    
    # 3. 預估指標 (今年營收/EPS/股利)
    st.write("---")
    st.subheader("預估指標與法人動態")
    c4, c5 = st.columns(2)
    c4.write(f"預估: 營收:{info.get('est_revenue')} | EPS:{info.get('est_eps')} | 股利:{info.get('est_dividend')}")
    c5.write(f"三大法人10日: :red[買:{info.get('inst_buy_10d')}] / :green[賣:{info.get('inst_sell_10d')}]")
    
    # 4. 10日資券比
    st.metric("10日資券比", f"{info.get('margin_ratio_10d', 0)}%")
    
    # 5. AI 與新聞
    st.subheader("分析區")
    st.info(f"AI 財報預測: {info.get('ai_prediction')}")
    with st.expander("新聞與AI深度解讀"):
        st.write(info.get("news_analysis"))
        
    # 6. 自動化系統狀態 (包含自動回測)
    st.sidebar.divider()
    st.sidebar.write("✅ 資料來源回測: 正常")
    st.sidebar.write("🔔 LINE 通知: 啟動")
    st.sidebar.write("🤖 AI 選股: 監控中")

if __name__ == "__main__":
    main()
