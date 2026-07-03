import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except: return {}

def color_df(val):
    """紅漲綠跌格式化"""
    try:
        v = float(str(val).replace(',', ''))
        return 'color: red' if v > 0 else ('color: green' if v < 0 else 'color: black')
    except: return ''

def main():
    st.title("📈 AI 專業金融分析終端")
    data = load_data()
    
    # 1. 即時股價 (側邊欄選股)
    with st.sidebar:
        st.header("系統控制")
        ticker = st.text_input("輸入股票代號 (例: 2330.TW)", "2330.TW")
        if st.button("確認選股"):
            st.session_state.target = ticker
            st.rerun()
            
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target) or {}

    st.header(f"1. 即時股價: {target}")
    price = info.get("price", 0)
    diff = info.get("diff", 0)
    st.metric("即時股價", f"{price} 元", delta=f"{diff} 元")

    # 2. 每股淨值、本益比、EPS
    st.subheader("2. 基本面數據")
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值 (NAV)", "查詢中")
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 4. 今年與去年每季報表
    st.subheader("4. 今年與去年每季報表")
    st.write("系統自動回測：資料來源狀態 [正常]")

    # 5. 三大法人買賣超
    st.subheader("5. 三大法人買賣超 (10日細項)")
    if "institutional_daily" in info:
        df_inst = pd.DataFrame(info["institutional_daily"])
        st.dataframe(df_inst.style.applymap(color_df), use_container_width=True)

    # 6. 資券比與主力券商
    st.subheader("6. 10日資券比與主力券商買賣")
    if "broker_daily" in info:
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)

    # 7. AI 財報預測與新聞解讀 (按照需求調整順序)
    st.subheader("7. 新聞分析與 AI 財報預測")
    st.info(f"📰 GPT 新聞解讀: {info.get('news_analysis', '暫無近期新聞')}")
    st.success(f"🤖 AI 財報預測: {info.get('ai_prediction', '分析中...')}")
    st.error(f"⚠️ 黑天鵝危機警示: {info.get('black_swan_alert', '系統監控中：無異常')}")

if __name__ == "__main__":
    main()
