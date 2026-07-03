import streamlit as st
import pandas as pd  # 修正：確保匯入 pandas
import json
import os            # 修正：確保匯入 os

# 設定頁面寬度
st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    # 使用絕對路徑讀取數據，避免路徑錯誤
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")
    if not os.path.exists(file_path):
        return None, f"找不到檔案: {file_path}"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as e:
        return None, f"讀取失敗: {str(e)}"

def main():
    st.title("📈 AI 智能金融監控終端")
    
    data, error = load_data()
    if error:
        st.error(error)
        return
    
    # 過濾掉 last_updated
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        st.subheader("選股搜尋")
        target = st.selectbox("選擇股票代號", tickers)
    
    info = data.get(target, {})
    if info:
        st.subheader(f"目標股票: {target}")
        
        # 顯示法人表格
        if "institutional_daily" in info:
            st.subheader("三大法人 10 日買賣超細項")
            st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
            
        # 顯示券商表格
        if "broker_daily" in info:
            st.subheader("10 家主力券商 10 日買賣超細項")
            st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)
    else:
        st.warning("查無此股票籌碼數據。")

if __name__ == "__main__":
    main()
