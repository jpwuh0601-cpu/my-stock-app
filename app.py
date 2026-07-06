import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    """從根目錄讀取 market_data.json"""
    file_path = os.path.join(os.getcwd(), "market_data.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception as e:
            st.error(f"資料解析失敗: {e}")
            return {}
    return {}

# 側邊欄輸入
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    data_cache = load_market_data()
    
    # 強制檢查 data_cache 是否為字典且含有該代號
    if isinstance(data_cache, dict) and ticker in data_cache:
        d = data_cache[ticker]
        
        # 確保 d 是一個字典，如果不是，則給予空字典，防止 .get() 報錯
        if not isinstance(d, dict):
            st.error(f"代號 {ticker} 的資料格式錯誤 (非字典格式)。")
        else:
            # 安全讀取每一個欄位
            price = d.get("price", 0)
            inst_data = d.get("institutional_data", [])
            ai_pred = d.get("ai_prediction", "暫無 AI 分析結果")
            
            st.success(f"已從離線資料庫載入 {ticker}")
            st.metric("最新股價", f"{float(price):.2f}")
            
            st.subheader("法人籌碼分析")
            if isinstance(inst_data, list) and len(inst_data) > 0:
                st.table(pd.DataFrame(inst_data))
            else:
                st.write("目前無法人籌碼資料")
            
            st.subheader("AI 深度分析")
            st.info(ai_pred)
    else:
        st.warning(f"資料庫中無此代號或資料異常: {ticker}")
        st.write("建議檢查 GitHub Actions 是否執行成功，或確認 tickers.txt 是否包含此代號。")
else:
    st.info("請輸入代號後點擊查詢。")
