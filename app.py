import streamlit as st
import json
import pandas as pd

st.set_page_config(layout="wide")

def load_data():
    with open("market_data.json", "r", encoding="utf-8") as f: return json.load(f)

def color_cells(val):
    color = 'red' if val > 0 else 'green'
    return f'color: {color}'

def main():
    st.title("📈 專業金融監控終端")
    data = load_data()
    
    # 1. 自選股與輸入區
    with st.sidebar:
        st.header("監控標的")
        ticker = st.selectbox("選擇股票", list(data.keys()))
        new_ticker = st.text_input("新增代號 (例如 2330.TW)")
        if st.button("確認選股"):
            st.session_state.target = new_ticker if new_ticker else ticker
            st.rerun()

    target = st.session_state.get("target", "2330.TW")
    info = data.get(target, {})

    # 2. 即時價格 (含顏色樣式)
    st.metric("即時股價", f"{info.get('price', 0)} 元")

    # 3. 三大法人與券商表格
    st.subheader("三大法人 10 日買賣超細項")
    if "institutional_data" in info:
        df_inst = pd.DataFrame(info["institutional_data"])
        st.dataframe(df_inst.style.map(color_cells, subset=['外資', '投信', '自營商']), use_container_width=True)

    st.subheader("主力券商 10 日買賣超細項")
    if "broker_data" in info:
        df_broker = pd.DataFrame(info["broker_data"])
        st.dataframe(df_broker.style.map(color_cells, subset=['券商A', '券商B']), use_container_width=True)

if __name__ == "__main__":
    main()
