import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="金融智慧終端")

def main():
    st.title("📈 專業金融智慧監控系統")
    
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    target = st.sidebar.text_input("輸入股票代號", "2330.TW")
    
    if target in data:
        info = data[target]
        
        # 警示區塊
        if info.get('black_swan') == "⚠️ 高風險警示":
            st.error(f"【嚴重警示】{target} 發生黑天鵝風險！")
        else:
            st.success(f"【系統狀態】{target} 運作安全。")
            
        # 指標區塊
        col1, col2, col3 = st.columns(3)
        col1.metric("EPS", info.get('eps', 0))
        col2.metric("本益比", info.get('pe', 0))
        col3.metric("每股淨值", info.get('nav', 0))
        
        # 籌碼視覺化 (新功能)
        st.subheader("5. 三大法人籌碼分析 (長條圖)")
        inst_data = info.get('institutional_data', [])
        if inst_data:
            df_inst = pd.DataFrame(inst_data)
            # 轉換資料格式以符合長條圖需求
            df_melt = df_inst.melt(id_vars="日期", var_name="法人", value_name="買賣超")
            fig = px.bar(df_melt, x="日期", y="買賣超", color="法人", barmode="group", 
                         title="法人近 10 日籌碼分佈")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("尚無法人籌碼統計資料。")
            
    else:
        st.write("請確認輸入正確代號且自動化排程已更新數據。")

if __name__ == "__main__":
    main()
