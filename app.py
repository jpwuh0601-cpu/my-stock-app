import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融監控終端")

def load_data():
    """使用絕對路徑讀取檔案，解決找不到檔案的問題"""
    # 取得當前 app.py 所在的資料夾路徑
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "market_data.json")
    
    if not os.path.exists(file_path):
        return None, f"找不到資料檔: {file_path}"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as e:
        return None, f"解析 JSON 錯誤: {str(e)}"

def main():
    st.title("📈 AI 智能金融監控終端")
    
    data, error = load_data()
    
    if error:
        st.error(error)
        st.info("💡 解決建議：請確認 GitHub Actions 的 Run workflow 是否已完成，且 market_data.json 有被成功提交到 main 分支。")
        return
        
    # 如果資料讀取成功
    tickers = [t for t in data.keys() if t != "last_updated"]
    
    with st.sidebar:
        st.subheader("選股搜尋")
        target = st.selectbox("請選擇或輸入股票代號", tickers)
    
    info = data.get(target, {})
    
    if info:
        st.subheader(f"目標股票: {target}")
        st.write("---")
        # 這裡會顯示您要求的法人與券商表格
        st.subheader("三大法人與主力券商籌碼細項")
        # 簡單除錯：印出 info 內容看看是否包含對應鍵值
        st.json(info) 
    else:
        st.warning("查無該股票籌碼數據。")

if __name__ == "__main__":
    main()
