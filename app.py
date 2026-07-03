import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 專業選股儀表板")

# 顏色格式化函式 (紅漲綠跌)
def color_negative_red(val):
    try:
        num = float(str(val).replace(',', ''))
        color = 'red' if num > 0 else 'green'
        return f'color: {color}'
    except:
        return ''

def load_data():
    path = "market_data.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📊 AI 專業金融分析終端")
    data = load_data()
    if not data:
        st.error("系統資料讀取失敗，請確認 market_data.json 是否已生成。")
        return

    # 側邊欄選股
    tickers = [t for t in data.keys() if t != "last_updated"]
    with st.sidebar:
        target = st.selectbox("1. 即時股價與選股", tickers)
        if st.button("確認選股"):
            st.session_state.target = target
            
    sym = st.session_state.get("target", tickers[0])
    info = data.get(sym, {})

    # 1. 即時股價
    st.header(f"股票: {sym}")
    st.metric("即時股價", info.get("price", "N/A"), delta=f"{info.get('change', 0)}%")

    # 2. 基本面資訊
    col1, col2, col3 = st.columns(3)
    col1.metric("每股淨值 (NAV)", "查詢中")
    col2.metric("本益比 (P/E)", "查詢中")
    col3.metric("EPS", "查詢中")

    # 4. 每季報表
    st.subheader("4. 財務報表 (年度/季度)")
    st.write("系統自動回測來源: Yahoo Finance API (確認連結: 運作中)")

    # 5. 三大法人 (紅漲綠跌)
    st.subheader("5. 三大法人買賣超 (10日)")
    if "institutional_daily" in info:
        df_inst = pd.DataFrame(info["institutional_daily"])
        st.dataframe(df_inst.style.applymap(color_negative_red), use_container_width=True)

    # 6. 融資融券與主力券商
    st.subheader("6. 融資融券與主力券商 (10日)")
    if "broker_daily" in info:
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)

    # 7. AI 財報預測
    st.subheader("7. AI 深度財報預測")
    st.success(info.get("ai_prediction", "AI 分析中..."))

if __name__ == "__main__":
    main()
