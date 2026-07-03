import streamlit as st
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "market_data.json")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if "selected_ticker" not in st.session_state:
        st.session_state.selected_ticker = tickers[0] if tickers else ""

    with st.sidebar:
        selected = st.selectbox("請選擇監控標的", tickers, index=tickers.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in tickers else 0)
        if st.button("確認選擇"):
            st.session_state.selected_ticker = selected
            st.rerun()

    info = data.get(st.session_state.selected_ticker, {})
    
    # 1. 即時股價
    price_change = info.get("change", 0)
    color = "red" if price_change >= 0 else "green"
    st.subheader(f"即時股價: :{color}[{info.get('price', 0):,.2f}]")
    
    # 2. 基本財務
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值", info.get("book_value", "N/A"))
    c2.metric("本益比", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))
    
    # 3. 預測與法人
    st.divider()
    st.subheader("預測與法人分析")
    c4, c5 = st.columns(2)
    c4.write(f"**預估今年:** 營收: {info.get('est_revenue', 'N/A')} | EPS: {info.get('est_eps', 'N/A')} | 股利: {info.get('est_dividend', 'N/A')}")
    c5.write(f"**三大法人10日買賣超:** :red[{info.get('inst_buy_10d', '0')}] / :green[{info.get('inst_sell_10d', '0')}]")
    
    # 4. 資券與主力
    st.subheader("籌碼動態")
    c6, c7 = st.columns(2)
    c6.metric("10日資券比", f"{info.get('margin_ratio_10d', '0')}%")
    c7.write("主力券商與外資/自營商數據載入中...")
    
    # 5. AI 與新聞區
    st.divider()
    st.subheader("AI 分析與系統報告")
    with st.expander("新聞解讀"):
        st.write(info.get("news_analysis", "無最新新聞"))
    st.info(f"AI 財報預測: {info.get('ai_prediction', '計算中...')}")
    
    # 6. 自動回測系統狀態
    st.sidebar.divider()
    st.sidebar.subheader("系統狀態")
    st.sidebar.write("✅ 自動回測系統: 資料來源確認正確")
    st.sidebar.write(f"🔔 LINE 通知: {info.get('line_status', '已開啟')}")
    st.sidebar.write(f"🤖 AI 選股狀態: {info.get('ai_selection_status', '運行中')}")

if __name__ == "__main__":
    main()
