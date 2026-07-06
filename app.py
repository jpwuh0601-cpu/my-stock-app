import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

# --- 資料讀取區 ---
def load_market_data():
    file_path = "market_data.json"
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

# --- 側邊欄與輸入 ---
raw_ticker = st.sidebar.text_input("輸入股票代號", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit(): ticker = f"{ticker}.TW"

# --- 主程式 ---
if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 確保 data_cache 是字典
    if not isinstance(data_cache, dict):
        st.error("資料庫格式錯誤")
    elif ticker not in data_cache:
        st.warning(f"找不到代號: {ticker}。請確認 GitHub Actions 是否已將此股票加入 JSON。")
    else:
        # 這裡使用安全的讀取方式
        d = data_cache.get(ticker)
        
        # 萬一 d 是 None 的極端情況處理
        if d is None:
            st.error(f"代號 {ticker} 存在但資料為空 (null)")
        else:
            # 1. 股價顯示
            st.metric("最新股價", f"{float(d.get('price', 0)):.2f}")
            
            # 2. 法人籌碼 (增加表格轉換保護)
            st.subheader("法人籌碼分析")
            inst_data = d.get("institutional_data")
            if isinstance(inst_data, list) and len(inst_data) > 0:
                try:
                    df = pd.DataFrame(inst_data)
                    st.table(df)
                except:
                    st.write("無法渲染表格資料")
            else:
                st.write("目前無法人籌碼資料")
            
            # 3. AI 分析
            st.subheader("AI 深度分析")
            st.info(d.get("ai_prediction") or "暫無分析數據")
else:
    st.info("請輸入代號後點擊查詢。")
