import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(layout="wide", page_title="AI 智能金融終端")

def load_data():
    # 嘗試讀取多種可能路徑
    possible_paths = ["market_data.json", "/app/market_data.json", "data/market_data.json"]
    
    # 除錯用：列出當前目錄所有檔案
    current_dir = os.getcwd()
    files_in_dir = os.listdir(current_dir)
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    
    st.error(f"找不到數據檔！當前目錄: {current_dir}")
    st.write(f"目錄下的檔案清單: {files_in_dir}")
    return {}

def main():
    data = load_data()
    # ... (其餘程式碼保持不變)
