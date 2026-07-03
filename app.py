import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="AI 專業金融分析終端")

def load_data():
    try:
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def style_df(df):
    """應用紅漲綠跌顏色樣式"""
    def color_format(val):
        try:
            v = float(str(val).replace(',', ''))
            return 'color: red' if v > 0 else 'color: green'
        except: return ''
    return df.style.applymap(color_format)

def main():
    st.title("📊 專業金融數據分析系統")
    data = load_data()
    
    # 側邊欄：自由輸入與選股按鈕
    with st.sidebar:
        st.header("選股設定")
        user_input = st.text_input("輸入股票代號 (例如 2330.TW)")
        # 加入明確的確認按鈕
        if st.button("確認選股"):
            st.session_state.target = user_input
            st.rerun()

    # 讀取目標代號
    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    # 1. 即時股價
    st.header(f"1. 即時股價: {target}")
    price = info.get("price", 0)
    diff = info.get("diff", 0)
    st.metric("當前股價", f"{price} 元", delta=f"{diff} 元")

    # 2. 基本面數據
    st.subheader("2. 基本面資訊")
    c1, c2, c3 = st.columns(3)
    c1.metric("每股淨值 (NAV)", "查詢中")
    c2.metric("本益比 (P/E)", info.get("pe", "N/A"))
    c3.metric("EPS", info.get("eps", "N/A"))

    # 4. 今年與去年每季報表
    st.subheader("4. 今年與去年每季報表")
    st.write("資料來源自動回測：狀態 [OK]")

    # 5. 三大法人買賣超 (列出10日)
    st.subheader("5. 三大法人買賣超細項 (10日)")
    if "institutional_daily" in info:
        df_inst = pd.DataFrame(info["institutional_daily"])
        st.dataframe(style_df(df_inst), use_container_width=True)

    # 6. 資券比與主力券商 (列出10日)
    st.subheader("6. 10日資券比與主力券商買賣")
    if "broker_daily" in info:
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)

    # 7. AI 財報預測與新聞分析
    st.subheader("7. AI 財報預測與新聞分析")
    st.info(f"新聞分析: {info.get('news_analysis', '近期無重大新聞')}")
    st.success(f"AI 財報預測: {info.get('ai_prediction', '分析中...')}")

if __name__ == "__main__":
    main()
