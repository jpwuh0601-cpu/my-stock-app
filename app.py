import streamlit as st
import pandas as pd
import json
import os  # 務必匯入此模組以解決 NameError
import plotly.express as px

st.set_page_config(layout="wide", page_title="金融智慧終端")

def main():
    st.title("📈 專業金融智慧監控系統")
    
    # 讀取數據檔案
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        st.warning("請確認 GitHub Actions 已同步資料至 market_data.json。")
        return

    # 側邊欄輸入
    target = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if target in data:
        info = data[target]
        
        # 狀態顯示
        if info.get('black_swan') == "⚠️ 高風險警示":
            st.error(f"【嚴重警示】{target} 發生黑天鵝風險！")
        else:
            st.success(f"【系統狀態】{target} 運作安全。")
            
        # 指標顯示
        col1, col2, col3 = st.columns(3)
        col1.metric("EPS", info.get('eps', 0))
        col2.metric("本益比", info.get('pe', 0))
        col3.metric("每股淨值", info.get('nav', 0))
        
        # 籌碼長條圖
        st.subheader("5. 三大法人籌碼分析")
        inst_data = info.get('institutional_data', [])
        if inst_data:
            df_inst = pd.DataFrame(inst_data)
            df_melt = df_inst.melt(id_vars="日期", var_name="法人", value_name="買賣超")
            fig = px.bar(df_melt, x="日期", y="買賣超", color="法人", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("查無此標的資訊，請確認代號是否在 tickers.txt 中。")

if __name__ == "__main__":
    main()
