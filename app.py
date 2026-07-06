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
            data = json.load(f)
            # 強制確保讀取到的資料是字典，如果不是，強制修正
            return data if isinstance(data, dict) else {}
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
        st.error("找不到 market_data.json，請檢查 GitHub Actions。")
    elif ticker not in data_cache:
        st.warning(f"找不到代號: {ticker}。目前清單: {list(data_cache.keys())}")
    else:
        d = data_cache[ticker]
        
        # 關鍵修正：如果 d 不是字典 (例如不小心變成了字串)，強制轉為空字典
        if not isinstance(d, dict):
            st.error(f"資料結構錯誤：{ticker} 的資料格式非字典，內容為: {type(d)}")
        else:
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
    st.info("請輸入代號後點擊查詢。")
