import streamlit as st
import pandas as pd
import json
import os  # 務必確保有這一行！
import plotly.express as px

st.set_page_config(layout="wide", page_title="金融智慧終端")

def main():
    st.title("📈 專業金融智慧監控系統")
    
    # 檢查檔案是否存在，避免程式崩潰
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                st.error("資料庫檔案格式錯誤，請等待自動化排程重新執行。")
                return
    else:
        st.warning("尚未抓取到市場資料，請稍候自動化系統完成更新。")
        return

    target = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", "2330.TW")
    
    if target in data:
        info = data[target]
        # 顯示警示
        if info.get('black_swan') == "⚠️ 高風險警示":
            st.error(f"【嚴重警示】{target} 發生黑天鵝風險！")
        else:
            st.success(f"【系統狀態】{target} 運作安全。")
            
        st.subheader("📊 財務數據分析")
        col1, col2, col3 = st.columns(3)
        col1.metric("EPS", info.get('eps', 0))
        col2.metric("本益比", info.get('pe', 0))
        col3.metric("每股淨值", info.get('nav', 0))
        
        st.subheader("5. 三大法人籌碼 (近10日)")
        df_inst = pd.DataFrame(info.get('institutional_data', []))
        st.dataframe(df_inst, use_container_width=True)
    else:
        st.write("查無此標的，請確認已加入 tickers.txt。")

if __name__ == "__main__":
    main()
