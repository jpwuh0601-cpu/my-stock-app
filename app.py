import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="金融智慧終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    st.title("📈 專業金融智慧監控系統")
    
    # 讀取現有資料
    data = load_data()
    
    # 側邊欄：自選股管理介面
    with st.sidebar.header("⚙️ 自選股管理"):
        new_ticker = st.text_input("新增觀察標的 (例如: 2317.TW)")
        if st.button("確認加入觀察清單"):
            if new_ticker:
                # 這裡實際應用應將 new_ticker 寫入 tickers.txt，目前先存入 session
                st.session_state.temp_tickers = new_ticker
                st.success(f"已加入 {new_ticker} 到觀察清單 (請等待下次自動化排程)")

    # 選擇股票
    ticker_list = list(data.keys()) if data else ["2330.TW"]
    target = st.selectbox("請選擇要分析的股票", ticker_list)
    
    if target in data:
        info = data[target]
        
        # 顯示警示
        if info.get('black_swan') == "⚠️ 高風險警示":
            st.error(f"🚨 {target} 發生黑天鵝風險")
        else:
            st.success(f"✅ {target} 運作安全")
            
        # 指標顯示
        col1, col2, col3 = st.columns(3)
        col1.metric("即時價格", info.get('price', 0))
        col2.metric("EPS", info.get('eps', 0))
        col3.metric("AI 市場觀點", info.get('ai_prediction', '分析中...'))
        
        # 籌碼圖表
        st.subheader("📊 法人籌碼趨勢")
        inst_data = info.get('institutional_data', [])
        if inst_data:
            df = pd.DataFrame(inst_data)
            fig = px.bar(df.melt(id_vars="日期"), x="日期", y="value", color="variable", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("數據載入中，請確認 GitHub Actions 是否已執行完成。")

if __name__ == "__main__":
    main()
