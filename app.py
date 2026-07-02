import streamlit as st
import pandas as pd
import json
import os

def load_data():
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    st.set_page_config(layout="wide", page_title="AI 智能金融終端")
    
    data = load_data()
    
    # 側邊欄：選股功能
    with st.sidebar:
        st.header("選股設定")
        stock_code = st.text_input("輸入股票代碼 (例如 2330.TW)")
        if st.button("確認選股"):
            st.session_state.selected_stock = stock_code
            
    # 頂部即時監控
    price = data.get("price", 0)
    change = data.get("change", 0)
    
    st.subheader("核心財務指標")
    cols = st.columns(4)
    cols[0].metric("即時股價", f"{float(price):,.2f}", delta=f"{float(change):.2f}")
    cols[1].metric("每股淨值", f"{float(data.get('bvps', 0)):.2f}")
    cols[2].metric("10日資券比", f"{float(data.get('margin_ratio', 0)):.2f}%")
    cols[3].metric("預估 EPS", f"{float(data.get('eps_forecast', 0)):.2f}")
        
    st.divider()

    # 籌碼面分析 (安全模式)
    st.subheader("三大法人與籌碼數據")
    df_inst = pd.DataFrame(data.get("institutional_investors", []))
    if not df_inst.empty:
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.write("目前無法人數據，請確認 worker.py 執行狀態。")

    st.subheader("AI 市場趨勢分析")
    st.info(data.get("ai_prediction", "AI 正在分析數據中..."))

if __name__ == "__main__":
    main()
