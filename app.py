import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def main():
    st.title("📈 AI 智能金融監控終端")
    data = load_data()
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    # 搜尋功能：輸入框優先，選單為輔
    user_input = st.text_input("輸入股票代號 (例如: 2330.TW)", "")
    selected_ticker = user_input if user_input in tickers else st.selectbox("選擇監控標的", tickers)
    
    info = data.get(selected_ticker, {})
    
    if info:
        # 股價顯示
        chg = info.get("change", 0)
        color = "red" if chg >= 0 else "green"
        st.markdown(f"## {selected_ticker} 即時股價: :{color}[{info.get('price', 0):,.2f}]")
        
        # 籌碼表格呈現
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("三大法人 10 日籌碼")
            st.table(pd.DataFrame(info.get("institutional_data", [])))
        with c2:
            st.subheader("10 家主力券商籌碼")
            st.table(pd.DataFrame(info.get("broker_data", [])))
    else:
        st.warning("查無此股票資料，請檢查代號或確認系統已執行更新。")

if __name__ == "__main__":
    main()
