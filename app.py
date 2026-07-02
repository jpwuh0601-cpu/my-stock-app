import streamlit as st
import pandas as pd
import json
import os

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    
    # 1. 側邊欄：選股功能
    with st.sidebar:
        st.header("選股設定")
        stock_code = st.text_input("輸入股票代碼 (例如 2330.TW)")
        if st.button("確認選股"):
            st.session_state.selected_stock = stock_code
        if "selected_stock" in st.session_state:
            st.success(f"已鎖定: {st.session_state.selected_stock}")
            
    data = load_data()
    
    # 2. 頂部即時監控 (漲紅跌綠邏輯)
    # 假設 data 中有 price 和 change (漲跌額)
    price = data.get("price", 2460.0)
    change = data.get("change", 15.0) 
    
    with st.container():
        cols = st.columns(4)
        # delta 正數顯示紅色，負數顯示綠色
        cols[0].metric("即時股價", f"{float(price):,.2f}", delta=f"{float(change):.2f}")
        cols[1].metric("每股淨值", f"{float(data.get('bvps', 150.2)):.2f}")
        cols[2].metric("10日資券比", f"{float(data.get('margin_ratio', 1.25)):.2f}%")
        cols[3].metric("預估 EPS", f"{float(data.get('eps_forecast', 73.65)):.2f}")
        
    st.divider()

    # 3. 籌碼面分析 (法人與主力)
    tab1, tab2 = st.tabs(["財務報表", "籌碼面分析"])
    
    with tab2:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("三大法人 10日累計買賣超")
            # 建立範例資料並進行樣式格式化 (漲紅跌綠)
            df_inst = pd.DataFrame({"機構": ["外資", "投信", "自營商"], "10日累計": [12500, 3200, -800]})
            def color_negative_red(val):
                color = 'red' if val > 0 else 'green'
                return f'color: {color}'
            st.dataframe(df_inst.style.applymap(color_negative_red, subset=['10日累計']), use_container_width=True)
            
        with col_right:
            st.subheader("10日資券比與主力券商")
            st.write("顯示主力券商 10 日買賣情況...")

    # 4. AI 深度解讀
    st.subheader("即時新聞與 AI 解讀")
    st.info("新聞標題...")
    st.success("AI 深度解讀: ...")

if __name__ == "__main__":
    main()
