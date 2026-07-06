import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    if data_cache is None:
        st.error("錯誤：找不到 market_data.json，請確認 GitHub Actions 是否執行成功。")
    elif not isinstance(data_cache, dict):
        st.error("錯誤：資料庫格式異常。")
    elif ticker in data_cache:
        d = data_cache[ticker]
        st.success(f"已載入 {ticker}")
        st.metric("最新股價", f"{float(d.get('price', 0)):.2f}")
        
        st.subheader("法人籌碼分析")
        inst_data = d.get("institutional_data", [])
        if isinstance(inst_data, list) and len(inst_data) > 0:
            st.table(pd.DataFrame(inst_data))
        else:
            st.write("目前無法人籌碼資料")
            
        st.subheader("AI 深度分析")
        st.info(d.get("ai_prediction", "暫無分析數據"))
    else:
        # 關鍵除錯功能：如果找不到代號，列出目前 JSON 裡有的代號
        available = list(data_cache.keys())
        st.warning(f"資料庫中無此代號: {ticker}")
        st.write(f"目前資料庫中包含的代號: `{', '.join(available)}`")
        st.write("若該股票不在清單中，請檢查 `tickers.txt` 並執行 GitHub Actions 更新。")
else:
    st.info("請輸入代號後點擊查詢。")
