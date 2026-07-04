import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="金融智慧終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def main():
    st.title("📈 專業金融智慧監控系統")
    
    # 1. 初始化 Session 用於臨時觀察清單
    if 'custom_tickers' not in st.session_state:
        st.session_state.custom_tickers = []

    # 2. 側邊欄：手動管理區
    with st.sidebar:
        st.header("⚙️ 標的管理")
        new_ticker = st.text_input("輸入股票代號 (例如: 2454.TW)")
        if st.button("確認加入觀察"):
            if new_ticker and new_ticker not in st.session_state.custom_tickers:
                st.session_state.custom_tickers.append(new_ticker)
                st.rerun() # 點擊後立即重刷介面
        
        st.write("---")
        st.write("目前自選清單:", st.session_state.custom_tickers)

    # 3. 讀取數據並顯示
    data = load_data()
    all_available = list(data.keys()) + st.session_state.custom_tickers
    
    target = st.selectbox("請選擇要分析的標的", all_available)
    
    if target in data:
        info = data[target]
        st.success(f"正在監控: {target}")
        
        # 指標卡片
        col1, col2, col3 = st.columns(3)
        col1.metric("即時價格", info.get("price", 0))
        col2.metric("EPS", info.get("eps", 0))
        col3.metric("本益比", info.get("pe", 0))
        
        # 籌碼圖表
        st.subheader("📊 三大法人籌碼分析")
        inst_data = info.get('institutional_data', [])
        if inst_data:
            df = pd.DataFrame(inst_data)
            fig = px.bar(df.melt(id_vars="日期"), x="日期", y="value", color="variable", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"目前 {target} 暫無即時數據，系統將在下次自動排程時嘗試載入。")

if __name__ == "__main__":
    main()
