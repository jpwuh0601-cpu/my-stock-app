import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path): 
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"讀取 JSON 失敗: {e}")
        return {}

ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data = load_market_data()
    d = data.get(ticker)
    
    if d is None:
        st.warning(f"找不到 '{ticker}'，目前 JSON 內的代號有: {list(data.keys())}")
    else:
        # 1. 財務數據顯示
        st.subheader("1. 基本財務數據")
        st.metric("即時股價", str(d.get('price', '0')))
        
        # 3. 三大法人買賣超 (強效清潔版)
        st.subheader("3. 三大法人買賣超")
        inst_data = d.get('institutional_data')
        
        # 【最嚴格檢查】：確保它是 list 且每一項都是 dict
        if isinstance(inst_data, list) and len(inst_data) > 0 and isinstance(inst_data[0], dict):
            try:
                # 建立 dataframe
                df = pd.DataFrame(inst_data)
                # 強制將所有內容轉字串，防止 Pandas 渲染出錯
                st.table(df.astype(str))
            except Exception as e:
                st.error(f"表格渲染失敗: {e}")
                st.write("原始資料結構:", inst_data)
        else:
            st.info("目前無有效的法人買賣超資料，原始內容如下：")
            st.write(inst_data) # 讓我們看看它究竟是什麼，以便修正 worker.py
            
        st.success("✅ 資料處理程序已執行完畢")
