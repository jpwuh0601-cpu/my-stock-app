import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path): 
        st.error(f"找不到檔案: {file_path}")
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"JSON 讀取失敗: {e}")
        return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 除錯顯示：列出 JSON 裡所有存在的鍵值，幫您找出代號不匹配的原因
    st.write("--- 除錯區 ---")
    st.write(f"您輸入的代號: '{ticker}'")
    st.write("JSON 內存在的代號列表:", list(data_cache.keys()))
    st.write("---")
    
    d = data_cache.get(ticker)
    
    if d is None:
        st.warning("查無該代號，請參考上方「JSON 內存在的代號列表」對照輸入。")
    else:
        # 使用 safe_float 處理所有數字欄位
        def safe_float(v):
            try: return float(v)
            except: return 0.0

        st.subheader("1. 基本財務數據")
        col1, col2, col3 = st.columns(3)
        col1.metric("即時股價", f"{safe_float(d.get('price')):.2f}")
        col2.metric("本益比", f"{safe_float(d.get('pe')):.2f}")
        col3.metric("每股盈餘", f"{safe_float(d.get('eps')):.2f}")

        # 3. 三大法人買賣超 (強效清潔版)
        st.subheader("3. 三大法人買賣超")
        inst_data = d.get('institutional_data')
        if isinstance(inst_data, list) and len(inst_data) > 0:
            df = pd.DataFrame(inst_data)
            # 強制轉換每一格為字串，完全解決 TypeError
            st.table(df.astype(str))
        else:
            st.write("目前無法人資料")
            
        st.success("✅ 資料已成功渲染")
else:
    st.info("請輸入代號後點擊「查詢分析數據」。")
