import streamlit as st
import pandas as pd
import json
import os  # 務必確保這行存在，這是解決錯誤的關鍵

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    # 使用 os 確保路徑讀取安全
    if os.path.exists("market_data.json"):
        try:
            with open("market_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"資料讀取失敗: {e}")
            return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    # 側邊欄：搜尋與選股按鈕
    with st.sidebar:
        st.subheader("搜尋設定")
        user_input = st.text_input("輸入股票代號 (例如: 2330.TW)")
        if st.button("確定選股"):
            st.session_state.target = user_input
    
    # 優先使用使用者搜尋的代號
    target = st.session_state.get("target", tickers[0] if tickers else "")
    info = data.get(target, {})

    if info:
        # 1. 即時股價與漲跌顏色
        chg = info.get("change", 0)
        color = "red" if chg >= 0 else "green"
        st.markdown(f"## {target} 即時股價: :{color}[{info.get('price', 0):,.2f}]")
        
        # 2. 三大法人每日細項表格
        st.subheader("三大法人 10 日每日張數細項")
        if "institutional_daily" in info:
            st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
        else:
            st.write("目前無法人每日資料")
            
        # 3. 10 家主力券商每日細項表格
        st.subheader("10 家主力券商 10 日每日張數細項")
        if "broker_daily" in info:
            st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)
        else:
            st.write("目前無主力券商資料")
            
    else:
        st.warning("查無此股票資料，請輸入正確代號並點擊「確定選股」，確認 GitHub Action 已成功執行。")

if __name__ == "__main__":
    main()
