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
    
    # 搜尋功能
    search = st.text_input("輸入股票代號 (例如: 2330.TW)", "")
    target = search if search in tickers else st.selectbox("監控標的", tickers)
    
    info = data.get(target, {})
    
    if info:
        # 即時股價與漲跌顏色
        chg = info.get("change", 0)
        color = "red" if chg >= 0 else "green"
        st.markdown(f"## {target} 即時股價: :{color}[{info.get('price', 0):,.2f}]")
        
        # 三大法人每日細項表格
        st.subheader("三大法人每日買賣超細項")
        st.dataframe(pd.DataFrame(info.get("institutional_daily", [])), use_container_width=True)
        
        # 主力券商每日細項表格
        st.subheader("主力券商每日買賣超細項")
        st.dataframe(pd.DataFrame(info.get("broker_daily", [])), use_container_width=True)
    else:
        st.warning("查無此股票資料，請檢查代號或確認 GitHub Action 已成功更新數據。")

if __name__ == "__main__":
    main()
