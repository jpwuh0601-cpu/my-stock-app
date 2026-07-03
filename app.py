import streamlit as st
import pandas as pd
import json
import os

# 確保所有必要的匯入都齊全
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    # 使用 os 確保檔案路徑安全
    data_path = os.path.join(os.path.dirname(__file__), "market_data.json")
    if os.path.exists(data_path):
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取資料發生錯誤: {e}")
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.info("系統正在同步數據，請稍候...")
        return

    # 搜尋與選擇介面
    with st.sidebar:
        st.subheader("搜尋設定")
        user_input = st.text_input("輸入股票代號 (例如: 2330.TW)")
        if st.button("確定搜尋"):
            st.session_state.target = user_input
    
    target = st.session_state.get("target", tickers[0])
    info = data.get(target, {})

    if info:
        st.markdown(f"## {target} 即時股價: :{ 'red' if info.get('change',0)>=0 else 'green' }[{info.get('price', 0):,.2f}]")
        
        # 法人細項表格
        st.subheader("三大法人 10 日每日張數細項")
        st.dataframe(pd.DataFrame(info.get("institutional_daily", [])), use_container_width=True)
        
        # 券商細項表格
        st.subheader("10 家主力券商 10 日每日張數細項")
        st.dataframe(pd.DataFrame(info.get("broker_daily", [])), use_container_width=True)
    else:
        st.warning("查無此代號，請確保輸入格式正確 (例如: 2330.TW) 並確認 Action 已更新數據。")

if __name__ == "__main__":
    main()
