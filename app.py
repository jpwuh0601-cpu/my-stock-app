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

# 側邊欄輸入
ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    d = data_cache.get(ticker)
    
    if d is None:
        st.warning(f"找不到代號 '{ticker}'。目前的資料庫包含: {list(data_cache.keys())}")
    else:
        # 1. 基本財務數據
        st.subheader("1. 基本財務數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", str(d.get('price', '0')))
        col2.metric("每股盈餘 (EPS)", str(d.get('eps', '0')))
        
        # 3. 三大法人買賣超 (最穩定的顯示邏輯)
        st.subheader("3. 三大法人買賣超")
        inst_data = d.get('institutional_data', [])
        
        if isinstance(inst_data, list) and len(inst_data) > 0:
            # 強制將每一筆資料轉換為純字串字典
            flat_data = []
            for item in inst_data:
                if isinstance(item, dict):
                    # 將字典內的所有值都轉為字串
                    flat_data.append({k: str(v) for k, v in item.items()})
                else:
                    # 如果不是字典，直接轉字串當作一欄顯示
                    flat_data.append({"資料": str(item)})
            
            df = pd.DataFrame(flat_data)
            st.table(df)
        else:
            st.write("目前沒有法人資料")

        # 6. AI 財報預測
        st.subheader("6. AI 財報預測")
        st.info(str(d.get('ai_prediction', '暫無數據')))
        
        st.success("✅ 資料已成功渲染")
else:
    st.info("請輸入代號後點擊查詢。")
