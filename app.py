import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="專業股市決策儀表板", layout="wide")
st.title("📈 專業股市決策儀表板")

def load_data():
    if os.path.exists("market_data.json"):
        with open("market_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號", "2330.TW")

# 自動修正代號格式 (如果使用者輸入 2002 而非 2002.TW)
ticker = raw_ticker
if not ticker.endswith(".TW") and not ticker.endswith(".TWO"):
    ticker += ".TW"

if st.sidebar.button("查詢分析"):
    data = load_data()
    
    if not data:
        st.error("市場數據庫檔案 market_data.json 不存在或為空，請先執行 main_task.py。")
    elif ticker in data:
        info = data[ticker]
        
        # 1. 股價資訊
        st.metric(label="即時股價", value=info.get('price', 0), delta=f"{info.get('change', 0)}")
        
        # 2. 基本財務數據
        st.subheader("1. 基本財務數據")
        c1, c2, c3 = st.columns(3)
        c1.metric("每股淨值", info.get('nav', 0))
        c2.metric("本益比", info.get('pe', 0))
        c3.metric("每股盈餘 (EPS)", info.get('eps', 0))
        
        # 3. 三大法人
        st.subheader("3. 三大法人買賣超 (10日)")
        if "institutional_data" in info:
            df = pd.DataFrame(info["institutional_data"])
            st.table(df)
        else:
            st.warning("目前無法人籌碼資料")
            
        # 6. AI 預測
        st.subheader("6. AI 財報預測")
        st.info(info.get("ai_prediction", "暫無分析數據"))
        st.success("資料來源驗證通過")
        
    else:
        st.error(f"查無代號為 {ticker} 的資料。")
        st.write("---")
        st.write("目前可查詢的代號列表：")
        st.write(list(data.keys()))
