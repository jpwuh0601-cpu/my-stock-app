import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path): return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

# 側邊欄
ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = load_market_data()
    d = data.get(ticker)
    
    if d is None:
        st.warning(f"找不到代號: {ticker}，請確認 JSON 檔案是否有資料。")
        # 除錯：直接把目前的 JSON 鍵值印出來給您看
        st.write("目前資料庫內的代號清單:", list(data.keys()))
    else:
        # 1. 財務數據 (強制轉字串，避免 NoneType 錯誤)
        st.subheader("1. 基本財務數據")
        st.metric("即時股價", str(d.get('price', '0')))
        
        # 3. 三大法人買賣超 (強效清潔版)
        st.subheader("3. 三大法人買賣超")
        inst_data = d.get('institutional_data', [])
        
        if isinstance(inst_data, list) and len(inst_data) > 0:
            # 建立 DataFrame
            df = pd.DataFrame(inst_data)
            # 【關鍵】將整份表格的所有內容強制轉為純字串，連 None 也變成 "None" 字串
            df_cleaned = df.fillna("0").applymap(lambda x: str(x))
            st.table(df_cleaned)
        else:
            st.write("目前沒有法人資料")
            st.json(d) # 把整包數據印出來檢查
