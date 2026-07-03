import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    # 這是修正關鍵：檢查當前環境的根路徑，並優先嘗試尋找 json 檔案
    # 嘗試多種可能存在的路徑
    possible_paths = [
        "market_data.json",                                # 本地執行
        os.path.join(os.getcwd(), "market_data.json"),     # 當前工作目錄
        "/mount/src/ai-stock-monitor/market_data.json"      # Streamlit Cloud 預設路徑
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f), None
            except Exception as e:
                return None, f"檔案存在但無法讀取: {str(e)}"
                
    return None, f"找不到檔案，嘗試了以下路徑: {possible_paths}"

def main():
    st.title("📈 AI 智能金融監控終端")
    
    data, error = load_data()
    
    if error:
        st.error(error)
        st.info("💡 請確認 GitHub Actions 執行時是否確實將 market_data.json 推送至 main 分支的根目錄。")
        return
    
    # 檢查是否成功讀取數據
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    if not tickers:
        st.warning("數據庫為空，請稍候。")
        return

    with st.sidebar:
        target = st.selectbox("選擇股票", tickers)
    
    info = data.get(target, {})
    
    st.subheader(f"分析目標: {target}")
    
    # 顯示數據表格
    if "institutional_daily" in info:
        st.subheader("三大法人 10 日買賣超細項")
        st.dataframe(pd.DataFrame(info["institutional_daily"]), use_container_width=True)
        
    if "broker_daily" in info:
        st.subheader("10 家主力券商 10 日買賣超細項")
        st.dataframe(pd.DataFrame(info["broker_daily"]), use_container_width=True)

if __name__ == "__main__":
    main()
