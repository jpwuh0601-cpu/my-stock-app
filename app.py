import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="金融智慧終端")

def main():
    st.title("📈 專業金融智慧監控系統")
    
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    target = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if target in data:
        info = data[target]
        
        # 1. 警示與即時資訊
        if info['black_swan'] == "⚠️ 高風險警示":
            st.error(f"【嚴重警示】{target} 發生黑天鵝風險！")
        else:
            st.success(f"【系統狀態】{target} 運作安全。")
            
        # 2. 財報報表優化顯示
        st.subheader("📊 財務數據分析")
        col1, col2, col3 = st.columns(3)
        col1.metric("EPS", info['eps'])
        col2.metric("本益比", info['pe'])
        col3.metric("每股淨值", info['nav'])
        
        # 3. 三大法人籌碼
        st.subheader("5. 三大法人籌碼 (近10日)")
        df_inst = pd.DataFrame(info['institutional_data'])
        st.dataframe(df_inst, use_container_width=True)
        
    else:
        st.write("查無資料，請確認自動化排程已執行。")

if __name__ == "__main__":
    main()
