import streamlit as st
import pandas as pd
import json
import os

# 設定網頁標題與排版
st.set_page_config(page_title="個股籌碼分析系統", layout="wide")
st.title("📈 個股籌碼分析系統")

def load_market_data():
    """
    載入市場數據，使用絕對路徑以確保讀取穩定
    若檔案不存在或 JSON 格式錯誤，回傳空字典
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    
    if not os.path.exists(file_path):
        return {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}

# 側邊欄輸入區
st.sidebar.header("查詢設定")
raw_ticker = st.sidebar.text_input("輸入股票代號 (例如: 2330.TW)", value="2330.TW")
ticker = raw_ticker.strip().upper()
if ticker.isdigit():
    ticker = f"{ticker}.TW"

if st.sidebar.button("查詢分析數據"):
    # 載入所有資料
    data_cache = load_market_data()
    
    # 檢查資料庫是否為空
    if not data_cache:
        st.error("系統錯誤：未讀取到有效的 market_data.json。請檢查 GitHub Actions 是否執行成功。")
    
    # 檢查代號是否存在
    elif ticker in data_cache:
        d = data_cache.get(ticker) or {}
        
        # 顯示即時股價
        price = d.get("price") or 0
        st.metric("最新股價", f"{float(price):.2f}")
        
        # 顯示法人籌碼 (加入防錯邏輯)
        st.subheader("法人籌碼分析")
        inst_data = d.get("institutional_data")
        
        if isinstance(inst_data, list) and len(inst_data) > 0:
            try:
                # 轉為 DataFrame 並清理不支援的型別 (如 dict)
                df = pd.DataFrame(inst_data)
                df = df.applymap(lambda x: str(x) if isinstance(x, (dict, list)) else x)
                st.table(df)
            except Exception:
                st.write("表格資料格式無法解析，請檢查數據結構。")
        else:
            st.write("目前無法人籌碼資料")
            
        # 顯示 AI 分析建議
        st.subheader("AI 深度分析")
        ai_prediction = d.get("ai_prediction") or "暫無 AI 分析結果。"
        st.info(ai_prediction)
        
    else:
        st.warning(f"查無資料：代號 {ticker} 不在目前的資料庫中。")
        st.write(f"目前資料庫內有的股票: {', '.join(data_cache.keys())}")

else:
    st.info("請輸入代號後點擊「查詢分析數據」按鈕。")
