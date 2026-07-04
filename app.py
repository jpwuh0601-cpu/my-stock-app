import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(layout="wide", page_title="專業金融監控終端")

def main():
    st.title("📈 專業金融監控終端系統")
    
    with open("market_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    target = st.sidebar.text_input("輸入股票代號", "2330.TW")
    
    if target in data:
        info = data[target]
        
        # 1. 即時股價
        st.markdown(f"### 目標: {target} | 即時股價: {info['price']}")
        
        # 2. 基本指標
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", info['nav'])
        c2.metric("本益比", info['pe'])
        c3.metric("EPS", info['eps'])
        
        # 3. 互動式 K 線圖 (歷史走勢)
        st.subheader("歷史走勢圖 (近一年)")
        df_hist = pd.DataFrame(info['history'])
        fig = px.line(df_hist, x='日期', y='股價', title=f"{target} 歷史股價走勢")
        st.plotly_chart(fig, use_container_width=True)
        
        # 4. 財報報表
        st.subheader("4. 財報報表")
        st.write("真實財務數據同步更新中...")
        
        # 5. 法人籌碼
        st.subheader("5. 三大法人買賣超")
        df_inst = pd.DataFrame(info['institutional_data'])
        st.dataframe(df_inst, use_container_width=True)

if __name__ == "__main__":
    main()
