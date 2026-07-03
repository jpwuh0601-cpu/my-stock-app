import streamlit as st
import pandas as pd
import json
import os  # 確保匯入 os 模組

# 設定頁面佈局
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """從 JSON 檔案安全讀取資料"""
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"讀取資料檔案時發生錯誤: {e}")
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    
    # 載入資料
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    # 搜尋設定介面
    with st.sidebar:
        st.subheader("搜尋設定")
        user_input = st.text_input("輸入股票代號 (例如: 2330.TW)")
        if st.button("確定選股"):
            st.session_state.target = user_input
    
    # 設定目標代號
    target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(target, {})

    if info:
        # 1. 即時股價與漲跌 (紅漲綠跌)
        chg = info.get("change", 0)
        color = "red" if chg >= 0 else "green"
        st.markdown(f"## {target} 即時股價: :{color}[{info.get('price', 0):,.2f}]")
        
        # 2. 三大法人 10 日細項
        st.subheader("三大法人 10 日買賣超 (每日張數細項)")
        if "institutional_daily" in info:
            st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
        
        # 3. 主力券商 10 日細項
        st.subheader("10 家主力券商 10 日買賣超 (每日張數細項)")
        if "broker_daily" in info:
            st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)
            
    else:
        st.warning("查無此股票資料，請確保代號正確並已透過 GitHub Action 完成更新。")

if __name__ == "__main__":
    main()
